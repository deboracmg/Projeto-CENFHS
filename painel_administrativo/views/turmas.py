from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
import json


from painel_administrativo.models.servicos import Aula, Matricula, Servico, Turma

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
    }

    return JsonResponse(dados)

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


def matriculas(request):
    matriculas = Matricula.objects.select_related("aluno", "turma__servico").all()

    return render(
        request,
        "painel/servicos/matriculas.html",
        {"matriculas": matriculas}
    )


def aulas(request):
    aulas = Aula.objects.select_related("turma").all()

    return render(
        request,
        "painel/servicos/aulas.html",
        {"aulas": aulas}
    )
