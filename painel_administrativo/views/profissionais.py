from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from painel_administrativo.models.pessoas import Profissional


def listar_profissionais(request):
    profissionais = Profissional.objects.all().order_by("-data_cadastro")
    return render(
        request,
        "painel/pessoas/profissionais.html",
        {"profissionais": profissionais}
    )


def detalhar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)
        
    dados = {
        "profissional_id": profissional.id,
        "cpf": profissional.cpf,
        "nome": profissional.nome,
        "data_nascimento": profissional.data_nascimento.strftime("%Y-%m-%d"),
        "telefone": profissional.telefone,
        "email": profissional.email,
        "area_atuacao": profissional.area_atuacao,
        "data_cadastro": profissional.data_cadastro,
    }

    return JsonResponse(dados)

def buscar_profissionais(request):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    termo = request.GET.get("q", "").strip()

    if termo:
        profissionais = Profissional.objects.filter(
            nome__icontains=termo,
        )[:10]
    else : 
        profissionais = Profissional.objects.filter(
        ).order_by("-data_cadastro")[:10]
    

    resultados = [
        {
            "id": profissional.id,
            "nome": profissional.nome,
        }
        for profissional in profissionais
    ]

    return JsonResponse({"resultados": resultados})


@transaction.atomic
def salvar_profissional(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        profissional_id = request.POST.get("profissional_id")

        if profissional_id:
            profissional = Profissional.objects.get(id=profissional_id)
            mensagem = "Profissional atualizado com sucesso."
        else:
            profissional = Profissional()
            mensagem = "Profissional cadastrado com sucesso."

        profissional.nome = request.POST.get("nome")
        profissional.cpf = request.POST.get("cpf")
        profissional.data_nascimento = request.POST.get("data_nascimento")
        profissional.telefone = request.POST.get("telefone")
        profissional.email = request.POST.get("email")
        profissional.area_atuacao = request.POST.get("area_atuacao")

        profissional.save()

        return JsonResponse({
            "sucesso": True,
            "profissional_id": profissional_id,
            "mensagem": mensagem
        }, status=200
        )

    except Exception as erro:
        print(f"Erro ao salvar profissional: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o profissional."
        }, status=500)

