import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.views.decorators.http import require_http_methods

from painel_administrativo.forms_galeria import SubstituirImagemForm
from painel_administrativo.models.galeria import (
    ImagemSite,
    POSICOES,
    IMAGENS_PADRAO,
)

logger = logging.getLogger(__name__)


def apagar_arquivo(storage, nome):
    try:
        storage.delete(nome)
    except OSError:
        logger.exception(
            'Não foi possível remover a imagem anterior da galeria.'
        )


@staff_member_required
@require_http_methods(['GET', 'POST'])
def galeria(request):
    formulario = None

    if request.method == 'POST':
        formulario = SubstituirImagemForm(request.POST, request.FILES)

        if formulario.is_valid():
            novo_nome = None
            storage = ImagemSite._meta.get_field('imagem').storage

            try:
                with transaction.atomic():
                    registro, _ = ImagemSite.objects.get_or_create(
                        posicao=formulario.cleaned_data['posicao'],
                        defaults={'imagem': ''},
                    )

                    registro = (
                        ImagemSite.objects
                        .select_for_update()
                        .get(pk=registro.pk)
                    )

                    nome_anterior = registro.imagem.name

                    registro.imagem.save(
                        formulario.cleaned_data['imagem'].name,
                        formulario.cleaned_data['imagem'],
                        save=False,
                    )

                    novo_nome = registro.imagem.name
                    registro.save()

                    if nome_anterior:
                        transaction.on_commit(
                            lambda: apagar_arquivo(storage, nome_anterior)
                        )

            except Exception:
                if novo_nome:
                    apagar_arquivo(storage, novo_nome)

                logger.exception('Falha ao substituir uma imagem do site.')

                formulario.add_error(
                    None,
                    'Não foi possível salvar a imagem. Tente novamente.',
                )

            else:
                messages.success(
                    request,
                    'Imagem substituída com sucesso. '
                    'A alteração já está disponível no site.',
                )
                return redirect('galeria_site')

    cadastradas = {
        item.posicao: item
        for item in ImagemSite.objects.all()
    }

    imagens = []

    for posicao, titulo in POSICOES:
        registro = cadastradas.get(posicao)

        if registro and registro.imagem:
            url = registro.imagem.url
        else:
            url = static(IMAGENS_PADRAO[posicao])

        imagens.append({
            'posicao': posicao,
            'titulo': titulo,
            'url': url,
            'personalizada': bool(registro and registro.imagem),
        })

    return render(
        request,
        'painel/galeria/index.html',
        {
            'imagens': imagens,
            'formulario': formulario,
        },
        status=400 if formulario and formulario.errors else 200,
    )