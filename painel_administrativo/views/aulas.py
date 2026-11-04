from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
import json


from painel_administrativo.models.servicos import Aula


def aulas(request):
    aulas = Aula.objects.select_related("turma").all()

    return render(
        request,
        "painel/servicos/aulas.html",
        {"aulas": aulas}
    )
