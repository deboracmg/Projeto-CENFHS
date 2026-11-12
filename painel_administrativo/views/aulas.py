from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count, Q
import json


from painel_administrativo.models.servicos import Aula, Frequencia, Matricula


def buscar_aulas(turma_id):
    aulas = (
        Aula.objects
        .filter(turma_id=turma_id)
        .annotate(
            total_presentes=Count(
                "frequencias",
                filter=Q(frequencias__presente=True)
            )
        )
        .order_by("-data")
    )
    
    dados_aulas = []
    for a in aulas:
        aula = {
            "id": a.id,
            "data": a.data,
            "turma_id": a.turma_id,
            "total_presentes": a.total_presentes,
        }

        dados_aulas.append(aula)

    return dados_aulas


def buscar_frequencias(request, aula_id):
    frequencias = (
        Frequencia.objects
        .filter(aula_id=aula_id)
        .values(
            "id",
            "presente",
            "aula_id",
            "matricula_id",
            "matricula__aluno__nome"
        )
        .order_by("matricula__aluno__nome")
    )

    return JsonResponse(list(frequencias), safe=False)


@transaction.atomic
def salvar_aula(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Método não permitido."
            }, status=405)

        aula_id = request.POST.get("aula_id")
        turma_id = request.POST.get("turma_id")
        data = request.POST.get("data")

        frequencias = json.loads(
            request.POST.get("frequencias", "[]")
        )

        if not turma_id or not data:
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Informe a turma e a data da aula."
            }, status=400)

        if aula_id:
            aula = Aula.objects.get(id=aula_id, turma_id=turma_id)
            aula.data = data
            mensagem = "Aula atualizada com sucesso."
        else:
            aula = Aula(
                turma_id=turma_id,
                data=data
            )
            mensagem = "Aula cadastrada com sucesso."

        aula.save()

        validar_matriculas(turma_id, frequencias)

        for frequencia in frequencias:
            Frequencia.objects.update_or_create(
                aula=aula,
                matricula_id=frequencia["matricula_id"],
                defaults={
                    "presente": frequencia["presente"]
                }
            )

        return JsonResponse({
            "sucesso": True,
            "aula_id": aula.id,
            "aulas": buscar_aulas(turma_id),
            "mensagem": mensagem
        })

    except Aula.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Aula não encontrada."
        }, status=404)

    except Exception as erro:
        print(f"Erro ao salvar aula: {erro}")
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar a aula."
        }, status=500)


def validar_matriculas(turma_id, frequencias):
    matriculas_ids = [
        f["matricula_id"] for f in frequencias
    ]

    matriculas_validas = set(
        Matricula.objects.filter(
            turma_id=turma_id,
            id__in=matriculas_ids
        ).values_list("id", flat=True)
    )

    if len(matriculas_validas) != len(set(matriculas_ids)):
        raise Exception("Existem matrículas inválidas para esta turma")


@transaction.atomic
def excluir_aula(request):
    if request.method != "DELETE":
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Método não permitido."
        }, status=405)

    dados = json.loads(request.body)

    aula_id = dados.get("aula_id")
    turma_id = dados.get("turma_id")

    if not aula_id or not turma_id:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Turma ou aula não informada."
        }, status=400)

    try:
        Aula.objects.get(id=aula_id,turma_id=turma_id).delete()

        return JsonResponse({
            "sucesso": True,
            "aula_id": int(aula_id),
            "turma_id": turma_id,
            "aulas": buscar_aulas(turma_id),
            "mensagem": "Aula e frequências excluídas com sucesso."
        }, status=200)

    except Aula.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Aula não encontrada."
        }, status=404)

    