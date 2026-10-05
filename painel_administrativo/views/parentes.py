from django.db import transaction
from django.http import JsonResponse

from painel_administrativo.models.pessoas import Parente, Parentesco


def buscar_parente_por_cpf(request):
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

    parente = Parente.objects.filter(cpf=cpf).first()

    if not parente:
        return JsonResponse({
            "encontrado": False
        }, status=404)

    return JsonResponse({
        "encontrado": True,
        "parente": {
            "parente_id": parente.id,

            "cpf": parente.cpf,
            "nome": parente.nome,
            "telefone": parente.telefone,
            "profissao": parente.profissao,
            "local_trabalho": parente.local_trabalho,
            "escolaridade": parente.escolaridade,
            "vivo": parente.vivo,
        }
    }, status=200)


def detalhar_parente(request, parente):
    dados = {
        "parentesco_id": parente.parentesco.id,
        "parente_id": parente.id,

        "cpf": parente.cpf,
        "nome": parente.nome,
        "telefone": parente.telefone,
        "profissao": parente.profissao,
        "local_trabalho": parente.local_trabalho,
        "escolaridade": parente.escolaridade,
        "vivo": parente.vivo,

        "parentesco": parente.parentesco,
        "responsavel": parente.responsavel,
        "contato_emergencia": parente.contato_emergencia,
    }

    return JsonResponse(dados)


@transaction.atomic
def salvar_parente(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        parente_id = request.POST.get("parente_id")
        aluno_id = request.POST.get("aluno_id")

        if parente_id:
            parente = Parente.objects.get(id=parente_id)
        else:
            parente = Parente()

        parente.nome = request.POST.get("nome_familiar")
        parente.cpf = request.POST.get("cpf_familiar")
        parente.telefone = request.POST.get("telefone_familiar")
        parente.profissao = request.POST.get("profissao_familiar")
        parente.local_trabalho = request.POST.get("local_trabalho_familiar")
        parente.escolaridade = request.POST.get("escolaridade_familiar") or None
        parente.vivo = request.POST.get("familiar_vivo") == "on"

        parente.save()

        dados_parentesco = {
            "parentesco": request.POST.get("parentesco_familiar"),
            "responsavel": request.POST.get("familiar_responsavel") == "on",
            "contato_emergencia": request.POST.get("familiar_emergencia") == "on",
        }

        parentesco, created = Parentesco.objects.update_or_create(
            aluno_id=aluno_id,
            parente_id=parente.id,
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
        print(f"Erro ao salvar parente: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o parente."
        }, status=500)


def buscar_familia(aluno_id):
    familia = Parentesco.objects.select_related("parente").filter(aluno_id=aluno_id)
    dados_familia = []
    for f in familia:
        dados_familia.append({
            "parente_id": f.parente_id,
            "parentesco": f.parentesco,
            "parentesco_id": f.id,
            "nome": f.parente.nome,
            "cpf": f.parente.cpf,
            "telefone": f.parente.telefone,
            "profissao": f.parente.profissao,
            "local_trabalho": f.parente.local_trabalho,
            "escolaridade": f.parente.escolaridade,
            "vivo": f.parente.vivo,
            "responsavel": f.responsavel,
            "contato_emergencia": f.contato_emergencia,
        })

    return dados_familia


@transaction.atomic
def excluir_parente(request):
    if request.method != "POST":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    aluno_id = request.POST.get("aluno_id")
    parente_id = request.POST.get("parente_id")

    if not aluno_id or not parente_id:
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Aluno ou familiar não informado."
            },
            status=400
        )

    Parentesco.objects.get(aluno_id=aluno_id, parente_id=parente_id).delete()

    possui_outros_relacionamentos = Parentesco.objects.filter(
                    parente_id=parente_id).exists()

    if not possui_outros_relacionamentos:
        Parente.objects.filter(id=parente_id).delete()

    dados_familia = buscar_familia(aluno_id)

    return JsonResponse({
        "sucesso": True,
        "parente_id": int(parente_id),
        "aluno_id": aluno_id,
        "familia": dados_familia,
        "mensagem": "Familiar excluído com sucesso."
    }, status=200)

