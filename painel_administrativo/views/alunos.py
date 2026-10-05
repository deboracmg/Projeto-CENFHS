from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from painel_administrativo.models.pessoas import Aluno, Parente, Saude, Socioeconomico
from painel_administrativo.views.parentes import buscar_familia

# Centro de Formação
def listar_alunos(request):
    alunos = Aluno.objects.only(
        "id",
        "nome",
        "cpf",
        "data_nascimento",
        "telefone",
        "data_cadastro",
    ).order_by("-data_cadastro")

    context = {
        "alunos": alunos,
        "generos": Aluno.Genero.choices,
        "racas": Aluno.Raca.choices,
        "zonas": Aluno.Zona.choices,
        "situacao_moradia": Socioeconomico.SituacaoMoradia.choices,
        "escolaridade": Parente.Escolaridade.choices
    }

    return render(
        request,
        "painel/pessoas/alunos.html",
        context
    )


def detalhar_aluno(request, id):
    aluno = Aluno.objects.select_related(
        "saude",
        "socioeconomico",
    ).get(id=id)

    dados_familia = buscar_familia(id)

    dados_saude = None
    if hasattr(aluno, "saude"):
        dados_saude = {
            "sus": aluno.saude.sus,
            "problema_saude": aluno.saude.problema_saude,
            "tratamento": aluno.saude.tratamento,
            "tipo_sanguineo": aluno.saude.tipo_sanguineo,
            "alergia": aluno.saude.alergia,
            "medicamento": aluno.saude.medicamento,
            "vacinas": aluno.saude.vacinas,
        }

    dados_socioeconomico = None
    if hasattr(aluno, "socioeconomico"):
        dados_socioeconomico = {
            "n_bolsa_familia": aluno.socioeconomico.n_bolsa_familia,
            "nis": aluno.socioeconomico.nis,
            "escola": aluno.socioeconomico.escola,
            "transporte": aluno.socioeconomico.transporte,
            "renda_familiar": str(aluno.socioeconomico.renda_familiar or ""),
            "situacao_moradia": aluno.socioeconomico.situacao_moradia,
            "qtd_moradores": aluno.socioeconomico.qtd_moradores,
        }

    dados = {
        "id": aluno.id,
        "nome": aluno.nome,
        "cpf": aluno.cpf,
        "rg": aluno.rg,
        "data_nascimento": aluno.data_nascimento.strftime("%Y-%m-%d"),
        "naturalidade": aluno.naturalidade,
        "genero": aluno.genero,
        "raca": aluno.raca,
        "n_certidao": aluno.n_certidao,
        "telefone": aluno.telefone,
        "email": aluno.email,
        "foto": aluno.foto.url if aluno.foto else "",
        "observacoes": aluno.observacoes,
        "autoriza_uso_imagem": aluno.autoriza_uso_imagem,
        "data_cadastro": aluno.data_cadastro.strftime("%d/%m/%Y"),

        "cep": aluno.cep,
        "rua": aluno.rua,
        "numero": aluno.numero,
        "bairro": aluno.bairro,
        "cidade": aluno.cidade,
        "uf": aluno.uf,
        "zona": aluno.zona,

        "saude": dados_saude,
        "socioeconomico": dados_socioeconomico,
        "familia": dados_familia
    }

    return JsonResponse(dados)


@transaction.atomic
def salvar_aluno(request):
    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,            
                "mensagem": "Método não permitido."
                },
                status=405,
            )

        aluno_id = request.POST.get("aluno_id")
        if aluno_id:
            mensagem = "Aluno atualizado com sucesso."
            aluno = Aluno.objects.get(id=aluno_id)
        else:
            mensagem = "Aluno cadastrado com sucesso."
            aluno = Aluno()

        
        aluno.nome = request.POST.get("nome")
        aluno.cpf = request.POST.get("cpf")
        aluno.rg = request.POST.get("rg")
        aluno.data_nascimento = request.POST.get("data_nascimento")
        aluno.naturalidade = request.POST.get("naturalidade")
        aluno.genero = request.POST.get("genero")
        aluno.raca = request.POST.get("raca")
        aluno.n_certidao = request.POST.get("n_certidao")
        aluno.telefone = request.POST.get("telefone")
        aluno.email = request.POST.get("email")

        aluno.cep = request.POST.get("cep")
        aluno.rua = request.POST.get("rua")
        aluno.numero = request.POST.get("numero")
        aluno.bairro = request.POST.get("bairro")
        aluno.cidade = request.POST.get("cidade")
        aluno.uf = request.POST.get("uf")
        aluno.zona = request.POST.get("zona") or None

        aluno.observacoes = request.POST.get("observacoes")
        aluno.autoriza_uso_imagem = (request.POST.get("autoriza_uso_imagem") == "on")

        remover_foto = request.POST.get("remover_foto") == "true"
        if remover_foto:
            if aluno.foto:
                aluno.foto.delete(save=False)
            aluno.foto = None

        elif request.FILES.get("foto"):
            aluno.foto = request.FILES.get("foto")

        if request.FILES.get("termo_autorizacao"):
            aluno.termo_autorizacao = request.FILES.get("termo_autorizacao")

        aluno.save()

        dados_saude = {
            "sus": request.POST.get("sus"),
            "problema_saude": request.POST.get("problema_saude"),
            "tratamento": request.POST.get("tratamento"),
            "tipo_sanguineo": request.POST.get("tipo_sanguineo"),
            "alergia": request.POST.get("alergia"),
            "medicamento": request.POST.get("medicamento"),
            "vacinas": request.POST.get("vacinas"),
        }

        # Só cria registro de saude se tiver alguma informação preenchida
        if any(dados_saude.values()):
            Saude.objects.update_or_create(
                aluno=aluno,
                **dados_saude
            )
        else:
            Saude.objects.filter(aluno=aluno).delete()     

        renda_familiar = request.POST.get("renda_familiar")
        qtd_moradores = request.POST.get("qtd_moradores")

        dados_socioeconomico = {
            "n_bolsa_familia": request.POST.get("n_bolsa_familia"),
            "nis": request.POST.get("nis"),
            "escola": request.POST.get("escola"),
            "transporte": request.POST.get("transporte"),
            "renda_familiar": int(renda_familiar) if renda_familiar else None,
            "situacao_moradia": request.POST.get("situacao_moradia") or None,
            "qtd_moradores": int(qtd_moradores) if qtd_moradores else None,
        }

        # Só cria registro socioeconomico se tiver alguma informação preenchida
        if any(dados_socioeconomico.values()):
            Socioeconomico.objects.update_or_create(
                aluno=aluno,
                **dados_socioeconomico
            )
        else:
            Socioeconomico.objects.filter(aluno=aluno).delete()

        return JsonResponse({
            "sucesso": True,
            "id": aluno.id,
            "mensagem": mensagem
        }, status=200)
    
    except Exception as erro:
        print(f"Erro ao salvar aluno: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o aluno."
        }, status=500)


