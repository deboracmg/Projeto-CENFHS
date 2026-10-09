from django.db import transaction
from django.http import JsonResponse

from painel_administrativo.models.pessoas import Paciente
from painel_administrativo.models.servicos import Tratamento, Avaliacao

@transaction.atomic
def salvar_tratamento(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405
            )

        tratamento_id = request.POST.get("tratamento_id")
        paciente_id = request.POST.get("paciente_id")

        if tratamento_id:
            tratamento = Tratamento.objects.get(id=tratamento_id)
            mensagem = "Tratamento atualizado com sucesso."
        else:
            tratamento = Tratamento()
            mensagem = "Tratamento adicionado com sucesso."

        tratamento.paciente = Paciente.objects.get(id=paciente_id)
        tratamento.data_entrada = request.POST.get("data_entrada")
        tratamento.data_saida = request.POST.get("data_saida") or None
        tratamento.tipo_paciente = request.POST.get("tipo_paciente")
        tratamento.tratamento = request.POST.get("tratamento")
        tratamento.n_sessoes = request.POST.get("n_sessoes")
        tratamento.acompanhante = request.POST.get("acompanhante")
        tratamento.telefone_acompanhante = request.POST.get("telefone_acompanhante")
        tratamento.registrado_por = request.POST.get("registrado_por")
        tratamento.observacoes = request.POST.get("observacoes")

        tratamento.save()

        dados_avaliacao = {
            "atendimento": request.POST.get("atendimento"),
            "infraestrutura": request.POST.get("infraestrutura"),
            "higiene": request.POST.get("higiene"),
            "alimentacao": request.POST.get("alimentacao"),
            "comunicacao": request.POST.get("comunicacao"),
            "acolhimento": request.POST.get("acolhimento"),
            "organizacao": request.POST.get("organizacao"),
            "gestao": request.POST.get("gestao"),
        }

        # Só cria registro de avaliacao se tiver alguma informação preenchida
        if any(dados_avaliacao.values()):
            avaliacao, created = Avaliacao.objects.update_or_create(
                tratamento=tratamento,
                defaults=dados_avaliacao
            )
            if created:
                mensagem = "Avaliação realizada com sucesso."

        dados_tratamentos = buscar_tratamentos(paciente_id)

        return JsonResponse({
            "sucesso": True,
            "paciente_id": paciente_id,
            "tratamentos": dados_tratamentos,
            "mensagem": mensagem
        }, status=200
        )

    except Exception as erro:
        print(f"Erro ao salvar tratamento: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o tratamento."
        }, status=500)
    

def buscar_tratamentos(paciente_id):
    tratamentos = (
        Tratamento.objects
        .filter(paciente_id=paciente_id)
        .select_related("avaliacao")
        .order_by("-data_entrada")
    )
    
    dados_tratamentos = []
    for t in tratamentos:
        tratamento = {
            "tratamento_id": t.id,
            "paciente_id": t.paciente_id,
            "data_entrada": t.data_entrada,
            "data_saida": t.data_saida,
            "tipo_paciente": t.tipo_paciente,
            "tratamento": t.tratamento,
            "n_sessoes": t.n_sessoes,
            "acompanhante": t.acompanhante,
            "telefone_acompanhante": t.telefone_acompanhante,
            "observacoes": t.observacoes,
            "registrado_por": t.registrado_por,
        }

        try:
            avaliacao = t.avaliacao
        except Avaliacao.DoesNotExist:
            avaliacao = None
        
        if avaliacao:
            tratamento.update({
                "avaliacao_id": avaliacao.id,
                "data_avaliacao": avaliacao.data_avaliacao.strftime("%d/%m/%Y"),
                "atendimento": avaliacao.atendimento,
                "infraestrutura": avaliacao.infraestrutura,
                "higiene": avaliacao.higiene,
                "alimentacao": avaliacao.alimentacao,
                "comunicacao": avaliacao.comunicacao,
                "acolhimento": avaliacao.acolhimento,
                "organizacao": avaliacao.organizacao,
                "gestao": avaliacao.gestao,
            })

        dados_tratamentos.append(tratamento)

    return dados_tratamentos
