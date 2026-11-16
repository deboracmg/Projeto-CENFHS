from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from painel_administrativo.models.servicos import Encontro, Servico

def listar_encontros(request):
    encontros = Encontro.objects.select_related("servico", "responsavel_interno"
                                            ).all().order_by("-data_hora")
    tipos_servico = [
        (valor, rotulo)
        for valor, rotulo in Servico.Tipo.choices
        if valor != Servico.Tipo.CURSO
    ]

    context = {
        "encontros": encontros,
        "tipo_servico": tipos_servico
    }
    return render(
        request,
        "painel/servicos/encontros.html",
        context
    )

def detalhar_encontro(request, id):
    encontro = Encontro.objects.select_related(
        "servico", "responsavel_interno").get(id=id)
        
    dados = {
        "encontro_id": encontro.id,
        "tipo": encontro.servico.tipo,
        "servico_id": encontro.servico.id,
        "nome": encontro.servico.nome,
        "local": encontro.local,
        "data_hora": encontro.data_hora,
        "profissional_id": encontro.responsavel_interno.id if encontro.responsavel_interno else None,
        "resp_interno": encontro.responsavel_interno.nome if encontro.responsavel_interno else None,
        "resp_externo": encontro.responsavel_externo,
        "qtd_participantes": encontro.qtd_participantes,
        "lista_presenca": encontro.lista_presenca.url if encontro.lista_presenca else "",
    }

    return JsonResponse(dados)

@transaction.atomic
def salvar_encontro(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        encontro_id = request.POST.get("encontro_id")

        if encontro_id:
            encontro = Encontro.objects.get(id=encontro_id)
            mensagem = "Encontro atualizado com sucesso."
        else:
            encontro = Encontro()
            mensagem = "Encontro cadastrado com sucesso."

        from datetime import datetime

        data = datetime.strptime(
            request.POST.get("data_encontro"),
            "%Y-%m-%d"
        ).date()

        hora = datetime.strptime(
            request.POST.get("hora_encontro"),
            "%H:%M"
        ).time()

        data_hora = timezone.make_aware(datetime.combine(data, hora))
        qtd_participantes = request.POST.get("qtd_participantes")

        encontro.servico_id = request.POST.get("servico_id")
        encontro.local = request.POST.get("local")
        encontro.data_hora = data_hora
        encontro.responsavel_interno_id = request.POST.get("profissional_id")
        encontro.responsavel_externo = request.POST.get("resp_externo")
        encontro.qtd_participantes = int(qtd_participantes) if qtd_participantes else None

        remover_lista = request.POST.get("remover_lista") == "true"
        if remover_lista:
            if encontro.lista_presenca:
                encontro.lista_presenca.delete(save=False)
            encontro.lista_presenca = None

        elif request.FILES.get("lista_presenca"):
            encontro.lista_presenca = request.FILES.get("lista_presenca")


        encontro.save()

        return JsonResponse({
            "sucesso": True,
            "encontro_id": encontro_id,
            "mensagem": mensagem
        }, status=200
        )

    except Exception as erro:
        print(f"Erro ao salvar encontro: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o encontro."
        }, status=500)
