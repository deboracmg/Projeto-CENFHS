from django import template
from django.templatetags.static import static

from painel_administrativo.models.galeria import ImagemSite, IMAGENS_PADRAO

register = template.Library()


@register.simple_tag(takes_context=True)
def imagem_site(context, posicao):
    if '_imagens_site' not in context.render_context:
        context.render_context['_imagens_site'] = {
            item.posicao: item
            for item in ImagemSite.objects.all()
        }

    registro = context.render_context['_imagens_site'].get(posicao)

    if registro and registro.imagem:
        return registro.imagem.url

    return static(IMAGENS_PADRAO[posicao])