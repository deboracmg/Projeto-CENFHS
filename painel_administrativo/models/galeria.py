from uuid import uuid4
from django.db import models

# As posições representam as fotos que já existem no site.
POSICOES = [
    ('galeria-1', 'Galeria 1 — Início e Sobre nós'),
    ('galeria-2', 'Galeria 2 — Início e Sobre nós'),
    ('galeria-3', 'Galeria 3 — Início e Sobre nós'),
    ('galeria-4', 'Galeria 4 — Sobre nós'),
    ('galeria-5', 'Galeria 5 — Sobre nós'),
    ('galeria-6', 'Galeria 6 — Sobre nós'),
    ('galeria-7', 'Brechó Solidário — Início e/ou Sobre nós'),
    ('galeria-8', 'Terapia comunitária — Início e/ou Sobre nós'),
    ('galeria-9', 'Turma de karatê — Início e/ou Sobre nós'),
    ('galeria-10', 'Aula de ioga — Início e/ou Sobre nós'),
    ('galeria-11', 'Aula de redação — Início e/ou Sobre nós'),
    ('galeria-12', 'Encontro de terapia — Início e/ou Sobre nós'),
    ('galeria-13', 'Atividade de karatê — Início e/ou Sobre nós'),
    ('galeria-14', 'Atividade de redação — Início e/ou Sobre nós'),
    ('galeria-15', 'Alunos de karatê — Início e/ou Sobre nós'),
    ('logo', 'Identidade visual — logotipo do site'),
    ('qrcode-doacao', 'Sobre nós — QR Code de doação'),
    ('atividade-karate', 'Foto de atividade — Início e Serviços'),
]

IMAGENS_PADRAO = {
    'galeria-1': 'site/img/fotos/brecho/brecho-3.jpg',
    'galeria-2': 'site/img/fotos/karate/karate-1.jpg',
    'galeria-3': 'site/img/fotos/terapia-comunitaria/terapia-comunitaria-2.jpg',
    'galeria-4': 'site/img/fotos/ioga/ioga-1.jpg',
    'galeria-5': 'site/img/fotos/redacao/redacao-2.jpg',
    'galeria-6': 'site/img/fotos/karate/karate-3.jpg',
    'galeria-7': 'site/img/fotos/brecho/brecho-1.jpg',
    'galeria-8': 'site/img/fotos/terapia-comunitaria/terapia-comunitaria-1.jpg',
    'galeria-9': 'site/img/fotos/karate/karate-4.jpg',
    'galeria-10': 'site/img/fotos/ioga/ioga-2.jpg',
    'galeria-11': 'site/img/fotos/redacao/redacao-3.jpg',
    'galeria-12': 'site/img/fotos/terapia-comunitaria/terapia-comunitaria-3.jpg',
    'galeria-13': 'site/img/fotos/karate/karate-5.jpg',
    'galeria-14': 'site/img/fotos/redacao/redacao-1.jpg',
    'galeria-15': 'site/img/fotos/karate/karate-2.jpg',
    'logo': 'site/img/logo.png',
    'qrcode-doacao': 'site/img/qrcode-doacao.png',
    'atividade-karate': 'site/img/fotos/karate/karate-3.jpg',
}

def caminho_imagem(instance, filename):
    extensao = filename.rsplit('.', 1)[-1].lower()
    return f'galeria_site/{uuid4().hex}.{extensao}'

class ImagemSite(models.Model):
    posicao = models.CharField(max_length=40, choices=POSICOES, unique=True)
    imagem = models.ImageField(upload_to=caminho_imagem)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_posicao_display()
