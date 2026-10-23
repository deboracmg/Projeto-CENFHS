
from datetime import date, datetime, timedelta

from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from painel_administrativo.models.servicos import (
    Encontro, 
    Frequencia, 
    Servico, 
    Tratamento, 
    Avaliacao
)


def dashboard(request):
    hoje = timezone.localdate()

    # Mês e ano escolhidos nos filtros
    try:
        mes = int(request.GET.get("mes", hoje.month))
        ano = int(request.GET.get("ano", hoje.year))

        if not 1 <= mes <= 12 or not 1 <= ano <= 9998:
            raise ValueError

    except (ValueError, TypeError):
        mes = hoje.month
        ano = hoje.year
    
    inicio_mes = date(ano, mes, 1)

    if mes == 12:
        proximo_mes = date(ano + 1, 1, 1)
    else:
        proximo_mes = date(ano, mes + 1, 1)

    inicio_ano_data = date(ano, 1, 1)
    proximo_ano_data = date(ano + 1, 1, 1)

    fuso = timezone.get_current_timezone()

    inicio_mes_hora = timezone.make_aware(
        datetime.combine(inicio_mes, datetime.min.time()), fuso
    )
    proximo_mes_hora = timezone.make_aware(
        datetime.combine(proximo_mes, datetime.min.time()), fuso
    )

    inicio_ano_hora = timezone.make_aware(
        datetime.combine(inicio_ano_data, datetime.min.time()), fuso
    )
    proximo_ano_hora = timezone.make_aware(
        datetime.combine(proximo_ano_data, datetime.min.time()), fuso
    )

    # Frequência média dos cursos
    frequencias = Frequencia.objects.filter(
        aula__turma__servico__tipo=Servico.Tipo.CURSO
    )

    frequencia_mensal = frequencias.filter(
        aula__data__gte=inicio_mes,
        aula__data__lt=proximo_mes
    ).aggregate(media=Avg("presente"))["media"]

    frequencia_anual = frequencias.filter(
        aula__data__gte=inicio_ano_data,
        aula__data__lt=proximo_ano_data
    ).aggregate(media=Avg("presente"))["media"]

    # Participações em atividades
    atividades = Encontro.objects.filter(
        servico__tipo=Servico.Tipo.ATIVIDADE
    )

    atividades_mensal = atividades.filter(
        data_hora__gte=inicio_mes_hora,
        data_hora__lt=proximo_mes_hora
    ).aggregate(total=Sum("qtd_participantes"))["total"]

    atividades_anual = atividades.filter(
        data_hora__gte=inicio_ano_hora,
        data_hora__lt=proximo_ano_hora
    ).aggregate(total=Sum("qtd_participantes"))["total"]

    # Participações em eventos
    eventos = Encontro.objects.filter(
        servico__tipo=Servico.Tipo.EVENTO
    )

    eventos_mensal = eventos.filter(
        data_hora__gte=inicio_mes_hora,
        data_hora__lt=proximo_mes_hora
    ).aggregate(total=Sum("qtd_participantes"))["total"]

    eventos_anual = eventos.filter(
        data_hora__gte=inicio_ano_hora,
        data_hora__lt=proximo_ano_hora
    ).aggregate(total=Sum("qtd_participantes"))["total"]

     # Pacientes em atendimento hoje
    tratamentos_hoje = Tratamento.objects.filter(
        data_entrada__lte=hoje
    ).filter(
        Q(data_saida__gte=hoje) | Q(data_saida__isnull=True)
    )

    pacientes_hoje = tratamentos_hoje.values(
        "paciente_id"
    ).distinct().count()

    acompanhantes_hoje = tratamentos_hoje.exclude(
        acompanhante__isnull=True
    ).exclude(
        acompanhante=""
    ).count()

    # Pacientes atendidos no ano selecionado
    inicio_ano = date(ano, 1, 1)
    fim_ano = date(ano, 12, 31)

    pacientes_anual = Tratamento.objects.filter(
        data_entrada__lte=fim_ano
    ).filter(
        Q(data_saida__gte=inicio_ano) |
        Q(data_saida__isnull=True)
    ).values("paciente_id").distinct().count()
    
    # Média das avaliações realizadas no ano selecionado
    avaliacoes_ano = Avaliacao.objects.filter(
        data_avaliacao__gte=inicio_ano_hora,
        data_avaliacao__lt=proximo_ano_hora
    )

    notas = [
        "atendimento",
        "infraestrutura",
        "higiene",
        "alimentacao",
        "comunicacao",
        "acolhimento",
        "organizacao",
        "gestao",
    ]

    medias = avaliacoes_ano.aggregate(
        **{campo: Avg(campo) for campo in notas}
    )

    valores = [
        valor for valor in medias.values()
        if valor is not None
    ]

    avaliacao_anual = (
        round(sum(valores) / len(valores), 1)
        if valores else None
    )

    # Próximos eventos cadastrados
    proximos_eventos = Encontro.objects.filter(
        servico__tipo=Servico.Tipo.EVENTO,
        data_hora__gte=timezone.now()
    ).select_related("servico").order_by("data_hora")[:10]

    contexto = {
        "mes": mes,
        "ano": ano,
        "meses": [
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
        ],
        "anos": range(max(1, hoje.year - 5), max(hoje.year, ano) + 2),

        "frequencia_mensal": (
            round(frequencia_mensal * 100, 1)
            if frequencia_mensal is not None else None
        ),
        "frequencia_anual": (
            round(frequencia_anual * 100, 1)
            if frequencia_anual is not None else None
        ),
        "atividades_mensal": atividades_mensal,
        "atividades_anual": atividades_anual,
        "eventos_mensal": eventos_mensal,
        "eventos_anual": eventos_anual,
        "pacientes_hoje": pacientes_hoje,
        "acompanhantes_hoje": acompanhantes_hoje,
        "pacientes_anual": pacientes_anual,
        "avaliacao_anual": avaliacao_anual,
        "proximos_eventos": proximos_eventos,
    }

    return render(request, "painel/dashboard.html", contexto)
