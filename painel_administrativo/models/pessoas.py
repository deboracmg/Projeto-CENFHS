from django.db import models

# Pessoas do centro de formação
class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=50, null=True, blank=True)
    foto = models.ImageField(upload_to="alunos/", blank=True, null=True)
    data_nascimento = models.DateField()
    naturalidade = models.CharField(max_length=100, null=True, blank=True)

    class Genero(models.TextChoices):
        MASCULINO = "MASCULINO", "Masculino"
        FEMININO = "FEMININO", "Feminino"
        OUTRO = "OUTRO", "Outro"
    genero = models.CharField(
        max_length=20,
        choices=Genero.choices
    )

    class Raca(models.TextChoices):
        BRANCA = "BRANCA", "Branca"
        PRETA = "PRETA", "Preta"
        PARDA = "PARDA", "Parda"
        AMARELA = "AMARELA", "Amarela"   
        INDIGENA = "INDIGENA", "Indígena" 
    raca = models.CharField(
        max_length=20,
        choices=Raca.choices
    )

    n_certidao = models.CharField(max_length=50)

    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Zona(models.TextChoices):
        RURAL = "RURAL", "Rural"
        URBANA = "URBANA", "Urbana"
    
    zona = models.CharField(
        max_length=15,
        choices=Zona.choices,
        blank=True,
        null=True
    )

    observacoes = models.TextField(blank=True)

    autoriza_uso_imagem = models.BooleanField(default=False)
    termo_autorizacao = models.ImageField(
        upload_to="termos_autorizacao/",
        blank=True,
        null=True
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    

class Familiar(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    vivo = models.BooleanField(default=True)
    profissao = models.CharField(max_length=100, blank=True)
    local_trabalho = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=20)

    class Escolaridade(models.TextChoices):
        ANALFABETO = "ANALFABETO", "Analfabeto"
        FUNDAMENTAL = "FUNDAMENTAL", "Fundamental"
        MEDIO = "MEDIO", "Médio"
        TECNICO = "TECNICO", "Técnico"
        SUPERIOR = "SUPERIOR", "Superior" 

    escolaridade = models.CharField(
        max_length=20,
        choices=Escolaridade.choices,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome

    class Meta():
            verbose_name_plural = 'familiares'
    
    
class Parentesco(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    familiar = models.ForeignKey(
        Familiar,
        on_delete=models.CASCADE
    )

    parentesco = models.CharField(max_length=50)
    responsavel = models.BooleanField(default=False)
    contato_emergencia = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "familiar"],
                name="unique_aluno_familiar"
            )
        ]

    def __str__(self):
        return f"{self.aluno} - {self.familiar}"
    
    
class Saude(models.Model):
    aluno = models.OneToOneField(
        Aluno,
        on_delete=models.CASCADE,
        related_name="saude"
    )

    sus = models.CharField(max_length=20, blank=True)
    problema_saude = models.TextField(blank=True)
    tratamento = models.TextField(blank=True)
    tipo_sanguineo = models.CharField(max_length=3, blank=True)
    alergia = models.TextField(blank=True)
    medicamento = models.TextField(blank=True)
    vacinas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'saúde'
        verbose_name_plural = 'saúdes'

    def __str__(self):
        return f"Saúde de {self.aluno.nome}"
    
    
class Socioeconomico(models.Model):
    aluno = models.OneToOneField(
        Aluno,
        on_delete=models.CASCADE,
        related_name="socioeconomico"
    )

    n_bolsa_familia = models.CharField(max_length=20, blank=True)
    nis = models.CharField(max_length=20, blank=True)
    escola = models.CharField(max_length=150, blank=True)
    transporte = models.CharField(max_length=100, blank=True)

    renda_familiar = models.PositiveIntegerField(null=True, blank=True)

    class SituacaoMoradia(models.TextChoices):
            PROPRIA = "PROPRIA", "Própria"
            ALUGADA = "ALUGADA", "Alugada"
            CEDIDA = "CEDIDA", "Cedida"

    situacao_moradia = models.CharField(
        max_length=30,
        choices=SituacaoMoradia.choices,
        blank=True,
        null=True
        )
    qtd_moradores = models.PositiveIntegerField(null=True ,blank=True)

    class Meta:
        verbose_name = 'socioeconômico'
        verbose_name_plural = 'socioeconômicos'

    def __str__(self):
        return f"Socioeconômico de {self.aluno.nome}"
    
    
class Profissional(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    area_atuacao = models.CharField(max_length=100)

    termo_adesao = models.ImageField(
        upload_to="termos_adesao/",
        blank=True,
        null=True
    )
    
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta():
        verbose_name_plural = 'profissionais'

    def __str__(self):
        return self.nome
    

# Pessoas da casa de apoio
class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=50, null=True, blank=True)
    data_nascimento = models.DateField()
    naturalidade = models.CharField(max_length=100, null=True, blank=True)

    class Genero(models.TextChoices):
        MASCULINO = "MASCULINO", "Masculino"
        FEMININO = "FEMININO", "Feminino"
        OUTRO = "OUTRO", "Outro"
    
    genero = models.CharField(
        max_length=20,
        choices=Genero.choices
    )
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    nome_mae = models.CharField(max_length=150, blank=True)
    nome_pai = models.CharField(max_length=150, blank=True)

    profissao = models.CharField(max_length=100, blank=True)

    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    