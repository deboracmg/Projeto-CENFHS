from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from painel_administrativo.models.pessoas import Paciente
from painel_administrativo.models.servicos import Avaliacao
from painel_administrativo.views.tratamentos import buscar_tratamentos


# Casa de Apoio
def listar_pacientes(request):
    pacientes = Paciente.objects.only(
        "id",
        "nome",
        "cpf",
        "data_nascimento",
        "telefone",
    ).order_by("-data_cadastro")

    context = {
        "pacientes": pacientes,
        "generos": Paciente.Genero.choices,
        "opcoes_avaliacao": Avaliacao.OPCOES_AVALIACAO,
    }

    return render(
        request,
        "painel/pessoas/pacientes.html",
        context
    )

def detalhar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)

    dados_tratamentos = buscar_tratamentos(id)

    dados = {
        "id": paciente.id,
        "nome": paciente.nome,
        "cpf": paciente.cpf,
        "rg": paciente.rg,
        "data_nascimento": paciente.data_nascimento.strftime("%Y-%m-%d"),
        "naturalidade": paciente.naturalidade,
        "genero": paciente.genero,
        "telefone": paciente.telefone,
        "email": paciente.email,
        "nome_mae": paciente.nome_mae,
        "nome_pai": paciente.nome_pai,
        "profissao": paciente.profissao,
        "data_cadastro": paciente.data_cadastro,

        "cep": paciente.cep,
        "rua": paciente.rua,
        "numero": paciente.numero,
        "bairro": paciente.bairro,
        "cidade": paciente.cidade,
        "uf": paciente.uf,

        "tratamentos": dados_tratamentos
    }

    return JsonResponse(dados)

@transaction.atomic
def salvar_paciente(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405,
            )

        paciente_id = request.POST.get("paciente_id")
        if paciente_id:
            mensagem = "Paciente atualizado com sucesso."
            paciente = Paciente.objects.get(id=paciente_id)
        else:
            mensagem = "Paciente cadastrado com sucesso."
            paciente = Paciente()

        paciente.nome = request.POST.get("nome")
        paciente.cpf = request.POST.get("cpf")
        paciente.rg = request.POST.get("rg")
        paciente.data_nascimento = request.POST.get("data_nascimento")
        paciente.naturalidade = request.POST.get("naturalidade")
        paciente.genero = request.POST.get("genero") or None
        paciente.telefone = request.POST.get("telefone")
        paciente.email = request.POST.get("email")
        paciente.nome_mae = request.POST.get("nome_mae")
        paciente.nome_pai = request.POST.get("nome_pai")
        paciente.profissao = request.POST.get("profissao")

        paciente.cep = request.POST.get("cep")
        paciente.rua = request.POST.get("rua")
        paciente.numero = request.POST.get("numero")
        paciente.bairro = request.POST.get("bairro")
        paciente.cidade = request.POST.get("cidade")
        paciente.uf = request.POST.get("uf")

        paciente.save()

        return JsonResponse({
            "sucesso": True,
            "id": paciente.id,
            "mensagem": mensagem
        }, status=200)
    
    except Exception as erro:
        print(f"Erro ao salvar paciente: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o paciente."
        }, status=500)
