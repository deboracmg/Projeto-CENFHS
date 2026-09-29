from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from painel_administrativo.models.pessoas import Parente, Parentesco


def buscar_parente(request):
    if request.method != "GET":
        return JsonResponse(
            {"erro": "Método não permitido."},
            status=405
        )

    cpf = request.GET.get("cpf", "").strip()

    if not cpf:
        return JsonResponse(
            {"erro": "CPF não informado."},
            status=400
        )

    try:
        parente = Parente.objects.get(cpf=cpf)

    except Parente.DoesNotExist:
        return JsonResponse(
            {"erro": "Nenhum familiar encontrado com esse CPF."},
            status=404
        )

    return JsonResponse({
        "id": parente.id,
        "nome": parente.nome,
        "cpf": parente.cpf,
        "telefone": parente.telefone,
        "profissao": parente.profissao,
        "local_trabalho": parente.local_trabalho,
        "escolaridade": parente.escolaridade,
        "vivo": parente.vivo,
    })


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

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido."},
            status=405
        )

    parente_id = request.POST.get("parente_id")
    aluno_id = request.POST.get("id_aluno_referencia")

    if parente_id:
        mensagem = "Familiar atualizado com sucesso."
        parente = Parente.objects.get(id=parente_id)
    else:
        mensagem = "Familiar cadastrado com sucesso."
        parente = Parente()

    parente.nome = request.POST.get("nome_familiar")
    parente.cpf = request.POST.get("cpf_familiar")
    parente.telefone = request.POST.get("telefone_familiar")
    parente.profissao = request.POST.get("profissao_familiar")
    parente.local_trabalho = request.POST.get("local_trabalho_familiar")
    parente.escolaridade = request.POST.get("escolaridade_familiar") or None
    parente.vivo = request.POST.get("familiar_vivo") == "on"

    parente.save()

    parentesco = {
        "parentesco": request.POST.get("parentesco_familiar"),
        "responsavel": request.POST.get("familiar_responsavel") == "on",
        "contato_emergencia": request.POST.get("familiar_emergencia") == "on",
    }

    Parentesco.objects.update_or_create(
        aluno_id=aluno_id,
        parente_id=parente.id,
        **parentesco
    )

    familiar = {
        "nome": parente.nome,
        "parentesco": parentesco["parentesco"],
        "responsavel": parentesco["responsavel"],
        "contato_emergencia": parentesco["contato_emergencia"],
    }

    return JsonResponse({
        "sucesso": True,
        "id": parente.id,
        "familiar": familiar,
        "mensagem": mensagem
    })


