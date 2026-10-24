from pathlib import Path
from django import forms
from .models.galeria import POSICOES

class SubstituirImagemForm(forms.Form):
    posicao = forms.ChoiceField(choices=POSICOES, widget=forms.HiddenInput)
    imagem = forms.ImageField(label='Nova imagem', widget=forms.FileInput(attrs={
        'accept': '.jpg,.jpeg,.png,.webp',
    }))

    def clean_imagem(self):
        imagem = self.cleaned_data['imagem']
        if imagem.size > 5 * 1024 * 1024:
            raise forms.ValidationError('A imagem deve ter no máximo 5 MB.')
        extensao = Path(imagem.name).suffix.lower()
        formatos = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG', '.webp': 'WEBP'}
        if extensao not in formatos or imagem.image.format != formatos[extensao]:
            raise forms.ValidationError('Envie uma imagem JPG, PNG ou WebP válida, com a extensão correspondente.')
        largura, altura = imagem.image.size
        if largura * altura > 25000000:
            raise forms.ValidationError('A imagem deve ter no máximo 25 milhões de pixels.')
        imagem.seek(0)
        return imagem
