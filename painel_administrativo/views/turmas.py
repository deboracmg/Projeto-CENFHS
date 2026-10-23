from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse


from painel_administrativo.models.servicos import Aula, Matricula, Servico, Turma

def listar_turmas(request):
    turmas = Turma.objects.select_related("responsavel").all().order_by("-data_cadastro")

    return render(
        request,
        "painel/servicos/turmas.html",
        {"turmas": turmas}
    )


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
