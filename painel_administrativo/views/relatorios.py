import csv
from datetime import date, datetime, time, timedelta
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe

from painel_administrativo.forms_relatorios import (
    FiltroEncontrosForm, FiltroPeriodoForm, FiltroTurmasForm,
)
from painel_administrativo.models.servicos import Aula, Encontro, Matricula, Servico, Tratamento


def filtrar_periodo(registros, campo, filtros, *, com_horario=False):
    inicio = filtros["data_inicio"]
    fim = filtros["data_fim"]
    if com_horario:
        # Use os limites do dia local, inclusive quando o banco armazena em UTC.
        fuso = timezone.get_current_timezone()
        if inicio:
            limite_inicial = timezone.make_aware(datetime.combine(inicio, time.min), fuso)
            registros = registros.filter(**{f"{campo}__gte": limite_inicial})
        if fim and fim < date.max:
            dia_seguinte = fim + timedelta(days=1)
            limite_final = timezone.make_aware(datetime.combine(dia_seguinte, time.min), fuso)
            registros = registros.filter(**{f"{campo}__lt": limite_final})
        return registros

    if inicio:
        registros = registros.filter(**{f"{campo}__gte": inicio})
    if fim:
        registros = registros.filter(**{f"{campo}__lte": fim})
    return registros


def filtrar_turmas(registros, filtros):
    if filtros["curso"]:
        registros = registros.filter(turma__servico=filtros["curso"])
    if filtros["turma"]:
        registros = registros.filter(turma=filtros["turma"])
    return registros


def consultar_matriculas(filtros):
    registros = filtrar_turmas(Matricula.objects.all(), filtros)
    registros = filtrar_periodo(registros, "data_matricula", filtros, com_horario=True)
    return (
        registros.values("turma_id", "turma__servico__nome", "turma__descricao")
        .annotate(total=Count("pk"))
        .order_by("turma__servico__nome", "turma__descricao", "turma_id")
        .values_list("turma__servico__nome", "turma__descricao", "total")
    )


def consultar_frequencia(filtros):
    registros = filtrar_turmas(Aula.objects.all(), filtros)
    registros = filtrar_periodo(registros, "data", filtros)
    mesma_turma = Q(frequencias__matricula__turma_id=F("turma_id"))
    return (
        registros.values("turma_id", "turma__servico__nome", "turma__descricao")
        .annotate(
            aulas=Count("pk", distinct=True),
            presencas=Count("frequencias", filter=mesma_turma & Q(frequencias__presente=True)),
            faltas=Count("frequencias", filter=mesma_turma & Q(frequencias__presente=False)),
        )
        .order_by("turma__servico__nome", "turma__descricao", "turma_id")
        .values_list("turma__servico__nome", "turma__descricao", "aulas", "presencas", "faltas")
    )


def consultar_encontros(filtros):
    registros = Encontro.objects.filter(servico__tipo__in=[Servico.Tipo.ATIVIDADE, Servico.Tipo.EVENTO])
    if filtros["servico"]:
        registros = registros.filter(servico=filtros["servico"])
    registros = filtrar_periodo(registros, "data_hora", filtros, com_horario=True)
    return (
        registros.values("servico_id", "servico__nome", "servico__tipo")
        .annotate(
            encontros=Count("pk"),
            sem_contagem=Count("pk", filter=Q(qtd_participantes__isnull=True)),
            participacoes=Sum("qtd_participantes"),
        )
        .order_by("servico__nome", "servico_id")
        .values_list("servico__nome", "servico__tipo", "encontros", "sem_contagem", "participacoes")
    )


def consultar_tratamentos(filtros):
    registros = filtrar_periodo(Tratamento.objects.all(), "data_entrada", filtros)
    return (
        registros.values("tipo_paciente")
        .annotate(
            tratamentos=Count("pk"),
            pacientes=Count("paciente_id", distinct=True),
            sessoes=Sum("n_sessoes"),
        )
        .order_by("tipo_paciente")
        .values_list("tipo_paciente", "tratamentos", "pacientes", "sessoes")
    )


RELATORIOS = {
    "matriculas": {
        "titulo": "Matrículas",
        "criterio": "Mostra o total de matrículas por turma, pela data da matrícula.",
        "colunas": ("Curso ou atividade", "Turma", "Matrículas"),
        "formulario": FiltroTurmasForm,
        "consulta": consultar_matriculas,
    },
    "frequencia": {
        "titulo": "Frequência",
        "criterio": (
            "Mostra aulas, presenças e faltas por turma. A taxa de presença considera apenas as chamadas registradas."
        ),
        "colunas": ("Curso ou atividade", "Turma", "Aulas", "Presenças", "Faltas", "Taxa de presença"),
        "formulario": FiltroTurmasForm,
        "consulta": consultar_frequencia,
    },
    "encontros": {
        "titulo": "Encontros",
        "criterio": (
            "Mostra encontros por atividade ou evento. O total soma as participações registradas em cada encontro."
        ),
        "colunas": ("Atividade ou evento", "Tipo", "Encontros", "Sem contagem", "Participações"),
        "formulario": FiltroEncontrosForm,
        "consulta": consultar_encontros,
    },
    "tratamentos": {
        "titulo": "Casa de Apoio",
        "criterio": (
            "Mostra tratamentos, pacientes distintos e sessões informadas por tipo de paciente e data de entrada."
        ),
        "colunas": ("Tipo de paciente", "Tratamentos", "Pacientes distintos", "Sessões informadas"),
        "formulario": FiltroPeriodoForm,
        "consulta": consultar_tratamentos,
    },
}


def formatar_linha(tipo, linha):
    if tipo == "frequencia":
        presencas, faltas = linha[-2:]
        chamadas = presencas + faltas
        taxa = f"{presencas / chamadas:.1%}".replace(".", ",") if chamadas else "—"
        return (*linha, taxa)
    if tipo == "encontros":
        nome, tipo_servico, *totais = linha
        linha = (nome, Servico.Tipo(tipo_servico).label, *totais)
    return tuple("—" if valor in (None, "") else valor for valor in linha)


def exportar_csv(tipo, colunas, registros):
    resposta = HttpResponse(content_type="text/csv; charset=utf-8")
    resposta["Content-Disposition"] = f'attachment; filename="relatorio-{tipo}.csv"'
    resposta.write("\ufeff")
    escritor = csv.writer(resposta, delimiter=";")
    escritor.writerow(colunas)
    for registro in registros.iterator():
        linha = formatar_linha(tipo, registro)
        # Textos cadastrados no painel devem abrir como texto em planilhas.
        escritor.writerow([
            f"'{valor}" if isinstance(valor, str) and valor.lstrip().startswith(("=", "+", "-", "@"))
            else valor
            for valor in linha
        ])
    return resposta


@never_cache
@require_safe
def relatorios(request, tipo="matriculas", slug=None):
    if slug is not None:
        tipo = slug
    if tipo not in RELATORIOS:
        raise Http404("Relatório não encontrado.")

    relatorio = RELATORIOS[tipo]
    formulario = relatorio["formulario"](request.GET)
    contexto = {
        "abas": [
            {"slug": slug, "titulo": item["titulo"], "ativa": slug == tipo}
            for slug, item in RELATORIOS.items()
        ],
        "tipo": tipo,
        "relatorio": relatorio,
        "formulario": formulario,
    }
    if not formulario.is_valid():
        return render(request, "painel/relatorios/index.html", contexto, status=400)

    registros = relatorio["consulta"](formulario.cleaned_data)
    if request.GET.get("formato") == "csv":
        return exportar_csv(tipo, relatorio["colunas"], registros)

    pagina = Paginator(registros, 25).get_page(request.GET.get("pagina"))
    parametros = urlencode({
        campo: formulario[campo].value()
        for campo in formulario.fields
        if formulario[campo].value()
    })
    contexto.update(
        pagina=pagina,
        linhas=[formatar_linha(tipo, linha) for linha in pagina.object_list],
        filtros_url=f"{parametros}&" if parametros else "",
    )
    return render(request, "painel/relatorios/index.html", contexto)
