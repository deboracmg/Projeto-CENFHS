from datetime import date, datetime

from django.db.models import Avg, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from painel_administrativo.models.pessoas import Aluno, Profissional
from painel_administrativo.models.servicos import (
    Aula,
    Avaliacao,
    Encontro,
    Frequencia,
    Matricula,
    Servico,
    Tratamento,
    Turma,
)

MESES = [
    (1, "Janeiro"),
    (2, "Fevereiro"),
    (3, "Março"),
    (4, "Abril"),
    (5, "Maio"),
    (6, "Junho"),
    (7, "Julho"),
    (8, "Agosto"),
    (9, "Setembro"),
    (10, "Outubro"),
    (11, "Novembro"),
    (12, "Dezembro"),
]

CAMPOS_AVALIACAO = [
    "atendimento",
    "infraestrutura",
    "higiene",
    "alimentacao",
    "comunicacao",
    "acolhimento",
    "organizacao",
    "gestao",
]


def _obter_anos_com_registros(hoje):
    anos = set()

    anos.update(
        Aula.objects.values_list("data__year", flat=True).distinct()
    )
    anos.update(
        Tratamento.objects.values_list("data_entrada__year", flat=True).distinct()
    )
    anos.update(
        Tratamento.objects.exclude(data_saida__isnull=True)
        .values_list("data_saida__year", flat=True)
        .distinct()
    )

    for data_hora in Encontro.objects.values_list("data_hora", flat=True):
        if data_hora:
            anos.add(timezone.localtime(data_hora).year)

    for data_avaliacao in Avaliacao.objects.values_list("data_avaliacao", flat=True):
        if data_avaliacao:
            anos.add(timezone.localtime(data_avaliacao).year)

    anos.discard(None)

    if not anos:
        return [hoje.year]

    return sorted(anos)


def _obter_periodo_filtro(request, anos_disponiveis, hoje):
    ano_padrao = (
        hoje.year if hoje.year in anos_disponiveis else anos_disponiveis[-1]
    )

    try:
        mes = int(request.GET.get("mes", hoje.month))
        if not 1 <= mes <= 12:
            mes = hoje.month
    except (ValueError, TypeError):
        mes = hoje.month

    try:
        ano = int(request.GET.get("ano", ano_padrao))
        if ano not in anos_disponiveis:
            ano = ano_padrao
    except (ValueError, TypeError):
        ano = ano_padrao

    inicio_mes = date(ano, mes, 1)
    proximo_mes = date(ano + 1, 1, 1) if mes == 12 else date(ano, mes + 1, 1)

    inicio_ano = date(ano, 1, 1)
    proximo_ano = date(ano + 1, 1, 1)

    fuso = timezone.get_current_timezone()

    inicio_mes_hora = timezone.make_aware(
        datetime.combine(inicio_mes, datetime.min.time()), fuso
    )
    proximo_mes_hora = timezone.make_aware(
        datetime.combine(proximo_mes, datetime.min.time()), fuso
    )
    inicio_ano_hora = timezone.make_aware(
        datetime.combine(inicio_ano, datetime.min.time()), fuso
    )
    proximo_ano_hora = timezone.make_aware(
        datetime.combine(proximo_ano, datetime.min.time()), fuso
    )

    return {
        "mes": mes,
        "mes_nome": dict(MESES)[mes],
        "ano": ano,
        "inicio_mes": inicio_mes,
        "proximo_mes": proximo_mes,
        "inicio_ano": inicio_ano,
        "proximo_ano": proximo_ano,
        "inicio_mes_hora": inicio_mes_hora,
        "proximo_mes_hora": proximo_mes_hora,
        "inicio_ano_hora": inicio_ano_hora,
        "proximo_ano_hora": proximo_ano_hora,
    }


def _calcular_indicadores_centro_formacao(periodo):
    # Cadastros estruturais
    total_alunos = Aluno.objects.count()
    total_matriculas = Matricula.objects.count()
    total_turmas = Turma.objects.count()
    total_profissionais = Profissional.objects.count()

    # Cursos: frequência média e aulas registradas
    aulas_cursos = Aula.objects.filter(
        turma__servico__tipo=Servico.Tipo.CURSO
    )
    aulas_mensal = aulas_cursos.filter(
        data__gte=periodo["inicio_mes"],
        data__lt=periodo["proximo_mes"],
    ).count()
    aulas_anual = aulas_cursos.filter(
        data__gte=periodo["inicio_ano"],
        data__lt=periodo["proximo_ano"],
    ).count()

    frequencias = Frequencia.objects.filter(
        aula__turma__servico__tipo=Servico.Tipo.CURSO
    )
    frequencia_mensal = frequencias.filter(
        aula__data__gte=periodo["inicio_mes"],
        aula__data__lt=periodo["proximo_mes"],
    ).aggregate(media=Avg("presente"))["media"]

    frequencia_anual = frequencias.filter(
        aula__data__gte=periodo["inicio_ano"],
        aula__data__lt=periodo["proximo_ano"],
    ).aggregate(media=Avg("presente"))["media"]

    # Atividades: participantes e encontros realizados
    atividades = Encontro.objects.filter(
        servico__tipo=Servico.Tipo.ATIVIDADE
    )
    atividades_mes_qs = atividades.filter(
        data_hora__gte=periodo["inicio_mes_hora"],
        data_hora__lt=periodo["proximo_mes_hora"],
    )
    atividades_ano_qs = atividades.filter(
        data_hora__gte=periodo["inicio_ano_hora"],
        data_hora__lt=periodo["proximo_ano_hora"],
    )

    atividades_mensal = (
        atividades_mes_qs.aggregate(total=Sum("qtd_participantes"))["total"] or 0
    )
    atividades_anual = (
        atividades_ano_qs.aggregate(total=Sum("qtd_participantes"))["total"] or 0
    )
    atividades_encontros_mensal = atividades_mes_qs.count()
    atividades_encontros_anual = atividades_ano_qs.count()

    # Eventos: participantes e eventos realizados no período
    eventos = Encontro.objects.filter(
        servico__tipo=Servico.Tipo.EVENTO
    )
    eventos_mes_qs = eventos.filter(
        data_hora__gte=periodo["inicio_mes_hora"],
        data_hora__lt=periodo["proximo_mes_hora"],
    )
    eventos_ano_qs = eventos.filter(
        data_hora__gte=periodo["inicio_ano_hora"],
        data_hora__lt=periodo["proximo_ano_hora"],
    )

    eventos_mensal = (
        eventos_mes_qs.aggregate(total=Sum("qtd_participantes"))["total"] or 0
    )
    eventos_anual = (
        eventos_ano_qs.aggregate(total=Sum("qtd_participantes"))["total"] or 0
    )
    eventos_realizados_mensal = eventos_mes_qs.count()
    eventos_realizados_anual = eventos_ano_qs.count()

    return {
        "total_alunos": total_alunos,
        "total_matriculas": total_matriculas,
        "total_turmas": total_turmas,
        "total_profissionais": total_profissionais,
        "aulas_mensal": aulas_mensal,
        "aulas_anual": aulas_anual,
        "frequencia_mensal": (
            round(float(frequencia_mensal) * 100, 1)
            if frequencia_mensal is not None
            else None
        ),
        "frequencia_anual": (
            round(float(frequencia_anual) * 100, 1)
            if frequencia_anual is not None
            else None
        ),
        "atividades_mensal": atividades_mensal,
        "atividades_anual": atividades_anual,
        "atividades_encontros_mensal": atividades_encontros_mensal,
        "atividades_encontros_anual": atividades_encontros_anual,
        "eventos_mensal": eventos_mensal,
        "eventos_anual": eventos_anual,
        "eventos_realizados_mensal": eventos_realizados_mensal,
        "eventos_realizados_anual": eventos_realizados_anual,
    }


def _contar_acompanhantes_unicos(tratamentos_qs):
    acompanhantes = tratamentos_qs.values_list(
        "cpf_acompanhante",
        "nome_acompanhante",
    )

    identificados = set()

    for cpf, nome in acompanhantes:
        cpf = (cpf or "").strip()
        nome = (nome or "").strip()

        if cpf:
            digitos_cpf = "".join(c for c in cpf if c.isdigit())
            if digitos_cpf:
                identificados.add(("cpf", digitos_cpf))
                continue

        if nome:
            identificados.add(("nome", nome.casefold()))

    return len(identificados)


def _filtrar_tratamentos_no_periodo(inicio_periodo, proximo_periodo, hoje):
    condicao_saida = Q(data_saida__gte=inicio_periodo)
    if inicio_periodo <= hoje:
        condicao_saida |= Q(data_saida__isnull=True)

    return Tratamento.objects.filter(
        data_entrada__lt=proximo_periodo
    ).filter(condicao_saida)


def _calcular_media_avaliacoes(avaliacoes_qs):
    medias = avaliacoes_qs.aggregate(
        **{campo: Avg(campo) for campo in CAMPOS_AVALIACAO}
    )
    valores = [
        float(valor) for valor in medias.values() if valor is not None
    ]

    if not valores:
        return None, None

    media = sum(valores) / len(valores)
    nota_arredondada = int(media + 0.5)
    rotulo = dict(Avaliacao.OPCOES_AVALIACAO).get(nota_arredondada, "")

    return round(media, 1), rotulo


def _calcular_indicadores_casa_apoio(periodo, hoje):
    # Atendimento hoje
    tratamentos_hoje = Tratamento.objects.filter(
        data_entrada__lte=hoje
    ).filter(
        Q(data_saida__gte=hoje) | Q(data_saida__isnull=True)
    )

    pacientes_hoje = tratamentos_hoje.values("paciente_id").distinct().count()
    acompanhantes_hoje = _contar_acompanhantes_unicos(tratamentos_hoje)

    # Atendimentos no mês e no ano selecionados
    tratamentos_mes_qs = _filtrar_tratamentos_no_periodo(
        periodo["inicio_mes"], periodo["proximo_mes"], hoje
    )
    tratamentos_ano_qs = _filtrar_tratamentos_no_periodo(
        periodo["inicio_ano"], periodo["proximo_ano"], hoje
    )

    pacientes_mensal = tratamentos_mes_qs.values("paciente_id").distinct().count()
    pacientes_anual = tratamentos_ano_qs.values("paciente_id").distinct().count()
    tratamentos_mensal = tratamentos_mes_qs.count()
    tratamentos_anual = tratamentos_ano_qs.count()

    # Avaliações no mês e no ano selecionados
    avaliacoes_mes_qs = Avaliacao.objects.filter(
        data_avaliacao__gte=periodo["inicio_mes_hora"],
        data_avaliacao__lt=periodo["proximo_mes_hora"],
    )
    avaliacoes_ano_qs = Avaliacao.objects.filter(
        data_avaliacao__gte=periodo["inicio_ano_hora"],
        data_avaliacao__lt=periodo["proximo_ano_hora"],
    )

    avaliacao_mensal, avaliacao_mensal_rotulo = _calcular_media_avaliacoes(
        avaliacoes_mes_qs
    )
    avaliacao_anual, avaliacao_anual_rotulo = _calcular_media_avaliacoes(
        avaliacoes_ano_qs
    )
    total_avaliacoes_mensal = avaliacoes_mes_qs.count()
    total_avaliacoes_anual = avaliacoes_ano_qs.count()

    return {
        "pacientes_hoje": pacientes_hoje,
        "acompanhantes_hoje": acompanhantes_hoje,
        "pacientes_mensal": pacientes_mensal,
        "pacientes_anual": pacientes_anual,
        "tratamentos_mensal": tratamentos_mensal,
        "tratamentos_anual": tratamentos_anual,
        "avaliacao_mensal": avaliacao_mensal,
        "avaliacao_mensal_rotulo": avaliacao_mensal_rotulo,
        "avaliacao_anual": avaliacao_anual,
        "avaliacao_anual_rotulo": avaliacao_anual_rotulo,
        "total_avaliacoes_mensal": total_avaliacoes_mensal,
        "total_avaliacoes_anual": total_avaliacoes_anual,
    }


def _buscar_proximos_eventos():
    return (
        Encontro.objects.filter(
            servico__tipo=Servico.Tipo.EVENTO,
            data_hora__gte=timezone.now(),
        )
        .select_related("servico", "responsavel_interno")
        .order_by("data_hora")[:10]
    )


def dashboard(request):
    hoje = timezone.localdate()
    anos_disponiveis = _obter_anos_com_registros(hoje)
    periodo = _obter_periodo_filtro(request, anos_disponiveis, hoje)

    contexto = {
        "mes": periodo["mes"],
        "mes_nome": periodo["mes_nome"],
        "ano": periodo["ano"],
        "meses": MESES,
        "anos": anos_disponiveis,
        **_calcular_indicadores_centro_formacao(periodo),
        **_calcular_indicadores_casa_apoio(periodo, hoje),
        "proximos_eventos": _buscar_proximos_eventos(),
    }

    return render(request, "painel/dashboard.html", contexto)
