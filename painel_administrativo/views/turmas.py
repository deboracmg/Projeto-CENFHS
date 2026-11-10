from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import json


from painel_administrativo.models.servicos import Turma, Matricula
from painel_administrativo.models.pessoas import Aluno
from painel_administrativo.views.matriculas import buscar_matriculas
from painel_administrativo.views.aulas import buscar_aulas


def listar_turmas(request):
    turmas = Turma.objects.select_related("responsavel").all().order_by("-data_cadastro")

    return render(
        request,
        "painel/servicos/turmas.html",
        {"turmas": turmas}
    )

def detalhar_turma(request, id):
    turma = Turma.objects.select_related(
        "servico", "responsavel").get(id=id)

    dados_matriculas = buscar_matriculas(id)
    dados_aulas = buscar_aulas(id)

    dados = {
        "id": turma.id,
        "descricao": turma.descricao,
        "curso_id": turma.servico.id,
        "curso_nome": turma.servico.nome,
        "professor_id": turma.responsavel.id,
        "professor_nome": turma.responsavel.nome,
        "local": turma.local,
        "dias_semana": turma.dias_semana,
        "hora_inicio": turma.hora_inicio,
        "hora_fim": turma.hora_fim,
        "data_cadastro": turma.data_cadastro,

        "matriculas": dados_matriculas,
        "aulas": dados_aulas
    }

    return JsonResponse(dados)

def buscar_alunos_nao_matriculados_na_turma(request, turma_id):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Método não permitido."
        }, status=405)

    termo = request.GET.get("q", "").strip()

    alunos = Aluno.objects.exclude(
        id__in=Matricula.objects.filter(
            turma_id=turma_id
        ).values("aluno_id")
    )

    if termo:
        alunos = alunos.filter(
            Q(nome__icontains=termo) |
            Q(cpf__icontains=termo)
        )

    alunos = alunos.order_by("-data_cadastro")[:10]

    resultados = [
        {
            "id": aluno.id,
            "nome": aluno.nome,
            "cpf": aluno.cpf,
        }
        for aluno in alunos
    ]

    return JsonResponse({"resultados": resultados})


def buscar_alunos_matriculados_na_turma(request, turma_id):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Método não permitido."
        }, status=405)

    alunos = Matricula.objects.filter(
            turma_id=turma_id
        ).values("id", "aluno__nome"
        ).order_by("aluno__nome")

    return JsonResponse(list(alunos), safe=False)


@transaction.atomic
def salvar_turma(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Método não permitido."
            }, status=405)

        turma_id = request.POST.get("turma_id")

        if turma_id:
            turma = Turma.objects.get(id=turma_id)
            mensagem = "Turma atualizada com sucesso."
        else:
            turma = Turma()
            mensagem = "Turma cadastrada com sucesso."

        dias_semana = json.loads(
            request.POST.get("dias_semana", "[]")
        )

        turma.servico_id = request.POST.get("curso_id")
        turma.responsavel_id = request.POST.get("professor_id")
        turma.descricao = request.POST.get("descricao")
        turma.local = request.POST.get("local")
        turma.hora_inicio = request.POST.get("hora_inicio")
        turma.hora_fim = request.POST.get("hora_fim")
        turma.dias_semana = dias_semana

        turma.save()

        return JsonResponse({
            "sucesso": True,
            "turma_id": turma_id,
            "mensagem": mensagem
        }, status=200)

    except Exception as erro:
        print(f"Erro ao salvar turma: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar a turma."
        }, status=500)
