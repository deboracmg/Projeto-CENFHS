from django.db import transaction
from django.http import JsonResponse

from painel_administrativo.models.pessoas import Familiar, Parentesco


def buscar_familiar_por_cpf(request):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    cpf = request.GET.get("cpf")

    if not cpf:
        return JsonResponse(
            {"erro": "CPF não informado."},
            status=400
        )

    familiar = Familiar.objects.filter(cpf=cpf).first()

    if not familiar:
        return JsonResponse({
            "encontrado": False
        })

    return JsonResponse({
        "encontrado": True,
        "familiar": {
            "familiar_id": familiar.id,

            "cpf": familiar.cpf,
            "nome": familiar.nome,
            "telefone": familiar.telefone,
            "profissao": familiar.profissao,
            "local_trabalho": familiar.local_trabalho,
            "escolaridade": familiar.escolaridade,
            "vivo": familiar.vivo,
        }
    }, status=200)


@transaction.atomic
def salvar_familiar(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        familiar_id = request.POST.get("familiar_id")
        aluno_id = request.POST.get("aluno_id")

        if familiar_id:
            familiar = Familiar.objects.get(id=familiar_id)
        else:
            familiar = Familiar()

        familiar.nome = request.POST.get("nome_familiar")
        familiar.cpf = request.POST.get("cpf_familiar")
        familiar.telefone = request.POST.get("telefone_familiar")
        familiar.profissao = request.POST.get("profissao_familiar")
        familiar.local_trabalho = request.POST.get("local_trabalho")
        familiar.escolaridade = request.POST.get("escolaridade_familiar") or None
        familiar.vivo = request.POST.get("familiar_vivo") == "on"

        familiar.save()

        dados_parentesco = {
            "parentesco": request.POST.get("parentesco"),
            "responsavel": request.POST.get("familiar_responsavel") == "on",
            "contato_emergencia": request.POST.get("familiar_emergencia") == "on",
        }

        parentesco, created = Parentesco.objects.update_or_create(
            aluno_id=aluno_id,
            familiar_id=familiar.id,
            defaults=dados_parentesco
        )

        if created:
            mensagem = "Familiar adicionado com sucesso."
        else:
            mensagem = "Familiar atualizado com sucesso."

        dados_familia = buscar_familia(aluno_id)

        return JsonResponse({
            "sucesso": True,
            "aluno_id": aluno_id,
            "familia": dados_familia,
            "mensagem": mensagem
        }, status=200
        )

    except Exception as erro:
        print(f"Erro ao salvar familiar: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o familiar."
        }, status=500)


def buscar_familia(aluno_id):
    familia = Parentesco.objects.select_related("familiar").filter(aluno_id=aluno_id)
    dados_familia = []
    for f in familia:
        dados_familia.append({
            "familiar_id": f.familiar_id,
            "parentesco": f.parentesco,
            "parentesco_id": f.id,
            "nome": f.familiar.nome,
            "cpf": f.familiar.cpf,
            "telefone": f.familiar.telefone,
            "profissao": f.familiar.profissao,
            "local_trabalho": f.familiar.local_trabalho,
            "escolaridade": f.familiar.escolaridade,
            "vivo": f.familiar.vivo,
            "responsavel": f.responsavel,
            "contato_emergencia": f.contato_emergencia,
        })

    return dados_familia


@transaction.atomic
def excluir_familiar(request):
    if request.method != "POST":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    aluno_id = request.POST.get("aluno_id")
    familiar_id = request.POST.get("familiar_id")

    if not aluno_id or not familiar_id:
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Aluno ou familiar não informado."
            },
            status=400
        )

    Parentesco.objects.get(aluno_id=aluno_id, familiar_id=familiar_id).delete()

    possui_outros_relacionamentos = Parentesco.objects.filter(
                    familiar_id=familiar_id).exists()

    if not possui_outros_relacionamentos:
        Familiar.objects.filter(id=familiar_id).delete()

    dados_familia = buscar_familia(aluno_id)

    return JsonResponse({
        "sucesso": True,
        "familiar_id": int(familiar_id),
        "aluno_id": aluno_id,
        "familia": dados_familia,
        "mensagem": "Familiar excluído com sucesso."
    }, status=200)

