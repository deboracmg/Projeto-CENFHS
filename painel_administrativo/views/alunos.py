import logging
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError

from painel_administrativo.models.pessoas import Aluno, Familiar, Saude, Socioeconomico
from painel_administrativo.models.servicos import Matricula
from painel_administrativo.views.familia import buscar_familia

logger = logging.getLogger(__name__)


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
        "escolaridade": Familiar.Escolaridade.choices
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
    dados_matriculas = _buscar_matriculas_aluno(id)

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
        "data_cadastro": aluno.data_cadastro,

        "cep": aluno.cep,
        "rua": aluno.rua,
        "numero": aluno.numero,
        "bairro": aluno.bairro,
        "cidade": aluno.cidade,
        "uf": aluno.uf,
        "zona": aluno.zona,

        "saude": dados_saude,
        "socioeconomico": dados_socioeconomico,
        "familia": dados_familia,
        "matriculas": dados_matriculas,
    }

    return JsonResponse(dados)


@transaction.atomic
def salvar_aluno(request):
    aluno = None
    foto_antiga = None
    remover_foto = False
    foto_enviada = None

    try:
        if request.method != "POST":
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Método não permitido."
                },
                status=405,
            )

        aluno_id = request.POST.get("aluno_id")
        cpf = (request.POST.get("cpf") or "").strip()

        cpf_existente = Aluno.objects.filter(cpf=cpf)
        if aluno_id:
            cpf_existente = cpf_existente.exclude(id=aluno_id)
        if cpf_existente.exists():
            return JsonResponse({
                "sucesso": False,
                "mensagem": "Já existe um aluno cadastrado com este CPF."
            }, status=400)

        if aluno_id:
            mensagem = "Aluno atualizado com sucesso."
            aluno = Aluno.objects.get(id=aluno_id)
        else:
            mensagem = "Aluno cadastrado com sucesso."
            aluno = Aluno()

        foto_antiga = (aluno.foto.storage, aluno.foto.name) if aluno.foto else None
        remover_foto = request.POST.get("remover_foto") == "true"
        foto_enviada = request.FILES.get("foto")

        if not remover_foto and foto_enviada:
            _validar_foto_aluno(foto_enviada)

        aluno.nome = request.POST.get("nome")
        aluno.cpf = cpf
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

        if remover_foto:
            aluno.foto = None
        elif foto_enviada:
            aluno.foto = foto_enviada

        if request.FILES.get("termo_autorizacao"):
            aluno.termo_autorizacao = request.FILES.get("termo_autorizacao")

        aluno.save()

        if foto_antiga and (remover_foto or foto_enviada):
            nome_atual = aluno.foto.name if aluno.foto else None
            if nome_atual != foto_antiga[1]:
                transaction.on_commit(
                    lambda antigo=foto_antiga: _apagar_arquivo_foto(*antigo)
                )

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
                defaults=dados_saude
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
                defaults=dados_socioeconomico
            )
        else:
            Socioeconomico.objects.filter(aluno=aluno).delete()

        return JsonResponse({
            "sucesso": True,
            "id": aluno.id,
            "mensagem": mensagem
        }, status=200)

    except ValidationError as erro:
        transaction.set_rollback(True)
        return JsonResponse({
            "sucesso": False,
            "mensagem": erro.message
        }, status=400)

    except Exception as erro:
        transaction.set_rollback(True)
        if (
            aluno is not None
            and not remover_foto
            and foto_enviada
            and aluno.foto
            and getattr(aluno.foto, "_committed", False)
            and (not foto_antiga or aluno.foto.name != foto_antiga[1])
        ):
            _apagar_arquivo_foto(aluno.foto.storage, aluno.foto.name)
        print(f"Erro ao salvar aluno: {erro}")

        return JsonResponse({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o aluno."
        }, status=500)


# Funções auxiliares
LIMITE_FOTO_BYTES = 2 * 1024 * 1024
FORMATOS_FOTO_PERMITIDOS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}


def _buscar_matriculas_aluno(aluno_id):
    mesma_turma = Q(frequencias__aula__turma_id=F("turma_id"))
    matriculas = (
        Matricula.objects
        .filter(aluno_id=aluno_id)
        .select_related("turma")
        .annotate(
            total_aulas=Count("frequencias", filter=mesma_turma, distinct=True),
            faltas=Count(
                "frequencias",
                filter=mesma_turma & Q(frequencias__presente=False),
                distinct=True,
            ),
        )
        .order_by("-data_matricula")
    )

    return [
        {
            "id": m.id,
            "turma": m.turma.descricao,
            "total_aulas": m.total_aulas,
            "faltas": m.faltas,
        }
        for m in matriculas
    ]


def _validar_foto_aluno(foto):
    if foto.size > LIMITE_FOTO_BYTES:
        raise ValidationError("A foto deve ter no máximo 2 MB.")

    extensao = Path(foto.name).suffix.lower()
    if extensao not in FORMATOS_FOTO_PERMITIDOS:
        raise ValidationError("Envie uma imagem JPG, PNG ou WebP válida.")

    try:
        with Image.open(foto) as imagem:
            formato = imagem.format
            imagem.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise ValidationError("O arquivo selecionado não é uma imagem válida.")
    finally:
        foto.seek(0)

    if formato != FORMATOS_FOTO_PERMITIDOS[extensao]:
        raise ValidationError(
            "Envie uma imagem JPG, PNG ou WebP válida, com a extensão correspondente."
        )


def _apagar_arquivo_foto(storage, nome):
    try:
        storage.delete(nome)
    except OSError:
        logger.exception("Não foi possível remover a foto do aluno.")


