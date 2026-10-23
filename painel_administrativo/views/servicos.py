from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse


from painel_administrativo.models.servicos import Aula, Matricula, Servico, Turma

def buscar_servicos(request):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    termo = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    if termo:
        servicos = Servico.objects.filter(
            ativo=True,
            tipo=tipo,
            nome__icontains=termo,
        )[:10]
    else : 
        servicos = Servico.objects.filter(
            ativo=True,
            tipo=tipo,
        ).order_by("-data_cadastro")[:10]
    

    resultados = [
        {
            "id": servico.id,
            "nome": servico.nome,
            "tipo": servico.get_tipo_display(),
        }
        for servico in servicos
    ]

    return JsonResponse({"resultados": resultados})

def detalhar_servico(request, id):
    servico = Servico.objects.get(id=id)
        
    dados = {
        "id": servico.id,
        "tipo": servico.tipo,
        "nome": servico.nome,
        "ativo": servico.ativo,
        "data_cadastro": servico.data_cadastro,
    }

    return JsonResponse(dados)

@transaction.atomic
def salvar_servico(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        servico_id = request.POST.get("servico_id")

        if servico_id:
            servico = Servico.objects.get(id=servico_id)
            mensagem = "Serviço atualizado com sucesso."
        else:
            servico = Servico()
            mensagem = "Serviço cadastrado com sucesso."

        servico.tipo = request.POST.get("tipo_servico")
        servico.nome = request.POST.get("nome")
        servico.ativo = request.POST.get("ativo") == "on"
        
        servico.save()

        return JsonResponse({
            "sucesso": True,
            "servico_id": servico_id,
            "mensagem": mensagem
        }, status=200
        )

    except Exception as erro:
        print(f"Erro ao salvar serviço: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o serviço."
        }, status=500)



def listar_cursos(request):
    cursos = Servico.objects.filter(tipo=Servico.Tipo.CURSO)

    return render(
        request,
        "painel/servicos/cursos.html",
        {"cursos": cursos}
    )


def listar_atividades(request):
    atividades = Servico.objects.filter(
        tipo=Servico.Tipo.ATIVIDADE
        ).order_by("-ativo", "-data_cadastro")

    return render(
        request,
        "painel/servicos/atividades.html",
        {"atividades": atividades}
    )


def listar_eventos(request):
    eventos = Servico.objects.filter(tipo=Servico.Tipo.EVENTO)

    return render(
        request,
        "painel/servicos/eventos.html",
        {"eventos": eventos}
    )


