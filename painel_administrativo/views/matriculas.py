from django.db import transaction
from django.http import JsonResponse
import json


from painel_administrativo.models.pessoas import Aluno
from painel_administrativo.models.servicos import Matricula, Turma


def buscar_matriculas(turma_id):
    matriculas = (
        Matricula.objects
        .filter(turma_id=turma_id)
        .select_related("aluno")
        .order_by("-data_matricula")
    )
    
    dados_matriculas = []
    for m in matriculas:
        matricula = {
            "matricula_id": m.id,
            "aluno_id": m.aluno.id,
            "aluno_nome": m.aluno.nome,
            "aluno_cpf": m.aluno.cpf,
            "turma_id": m.turma_id,
            "data_matricula": m.data_matricula,
            "matriculado_por": m.matriculado_por,
        }

        dados_matriculas.append(matricula)

    return dados_matriculas


@transaction.atomic
def excluir_matricula(request):
    if request.method != "DELETE":
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Método não permitido."
        }, status=405)

    dados = json.loads(request.body)

    turma_id = dados.get("turma_id")
    matricula_id = dados.get("matricula_id")

    if not turma_id or not matricula_id:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Turma ou matrícula não informada."
        }, status=400)

    try:
        Matricula.objects.get(turma_id=turma_id, id=matricula_id).delete()

        dados_matriculas = buscar_matriculas(turma_id)

        return JsonResponse({
            "sucesso": True,
            "matricula_id": int(matricula_id),
            "turma_id": turma_id,
            "matriculas": dados_matriculas,
            "mensagem": "Matrícula excluída com sucesso."
        }, status=200)

    except Matricula.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Matrícula não encontrada."
        }, status=404)


@transaction.atomic
def salvar_matricula(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Método não permitido."
            }, status=405)

        matricula_id = request.POST.get("matricula_id")
        turma_id = request.POST.get("turma_id")
        aluno_id = request.POST.get("aluno_id")

        if not turma_id or not aluno_id:
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Turma ou aluno não informado."
            }, status=400)

        if matricula_id:
            matricula = Matricula.objects.get(id=matricula_id)
            mensagem = "Matrícula atualizada com sucesso."
        else:
            if Matricula.objects.filter(turma_id=turma_id,aluno_id=aluno_id).exists():
                return JsonResponse({
                    "sucesso": False,
                    "mensagem": "Este aluno já está matriculado nesta turma."
                }, status=400)

            matricula = Matricula()
            mensagem = "Matrícula adicionada com sucesso."

        matricula.turma = Turma.objects.get(id=turma_id)
        matricula.aluno = Aluno.objects.get(id=aluno_id)
        matricula.matriculado_por = request.POST.get("matriculado_por")

        matricula.save()

        dados_matriculas = buscar_matriculas(turma_id)

        return JsonResponse({
            "sucesso": True,
            "turma_id": turma_id,
            "matriculas": dados_matriculas,
            "mensagem": mensagem
        }, status=200)

    except Matricula.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Matrícula não encontrada."
        }, status=404)

    except Turma.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Turma não encontrada."
        }, status=404)

    except Aluno.DoesNotExist:
        return JsonResponse({
            "sucesso": False,
            "mensagem": "Aluno não encontrado."
        }, status=404)

    except Exception as erro:
        print(f"Erro ao salvar matrícula: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar a matrícula."
        }, status=500)

