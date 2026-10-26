from django.db import models
from .pessoas import Aluno, Paciente, Profissional


# Serviços do centro de formação
class Servico(models.Model):

    class Tipo(models.TextChoices):
        CURSO = "CURSO", "Curso"
        ATIVIDADE = "ATIVIDADE", "Atividade"
        EVENTO = "EVENTO", "Evento"

    nome = models.CharField(max_length=150)
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices
    )
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'

    def __str__(self):
        return self.nome
    
    
class Encontro(models.Model):
    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="encontros"
    )

    responsavel_interno = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="encontros"
    )

    responsavel_externo = models.CharField(
        max_length=150,
        blank=True
    )

    data_hora = models.DateTimeField()
    local = models.CharField(max_length=150)
    qtd_participantes = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    lista_presenca = models.FileField(
        upload_to="listas_presenca/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.servico.nome} - {self.data_hora}"
    
    
class Turma(models.Model):
    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="turmas"
    )

    descricao = models.CharField(max_length=150)

    class DiaSemana(models.TextChoices):
        DOM = "DOM", "Domingo"
        SEG = "SEG", "Segunda"
        TER = "TER", "Terça"
        QUA = "QUA", "Quarta"
        QUI = "QUI", "Quinta"
        SEX = "SEX", "Sexta"
        SAB = "SAB", "Sábado"

    dias_semana = models.JSONField(default=list)

    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    local = models.CharField(max_length=150)

    responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name="turmas"
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servico.nome} - {self.descricao}"


class Matricula(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.PROTECT,
        related_name="matriculas"
    )

    turma = models.ForeignKey(
        Turma,
        on_delete=models.PROTECT,
        related_name="matriculas"
    )

    data_matricula = models.DateTimeField(auto_now_add=True)

    matriculado_por = models.CharField(max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "turma"],
                name="unique_aluno_turma"
            )
        ]
        verbose_name = 'matrícula'
        verbose_name_plural = 'matrículas'

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma}"

    
class Aula(models.Model):
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="aulas"
    )

    data = models.DateField()

    def __str__(self):
        return f"{self.turma} - {self.data}"
    

class Frequencia(models.Model):
    matricula = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE,
        related_name="frequencias"
    )

    aula = models.ForeignKey(
        Aula,
        on_delete=models.CASCADE,
        related_name="frequencias"
    )

    presente = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["matricula", "aula"],
                name="unique_matricula_aula"
            )
        ]
        verbose_name = 'frequência'
        verbose_name_plural = 'frequências'

    def __str__(self):
        return f"{self.matricula} - {self.aula}"



# Serviços da casa de apoio
class Tratamento(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name="tratamentos"
    )

    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)

    tipo_paciente = models.CharField(max_length=50)
    tratamento = models.CharField(max_length=150)
    n_sessoes = models.PositiveIntegerField(null=True, blank=True)

    observacoes = models.TextField(blank=True)

    acompanhante = models.CharField(max_length=150, blank=True)
    telefone_acompanhante = models.CharField(max_length=20, blank=True)

    registrado_por = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.paciente.nome} - {self.tratamento}"


class Avaliacao(models.Model):
    OPCOES_AVALIACAO = [
        (5, "Ótimo"),
        (4, "Bom"),
        (3, "Regular"),
        (2, "Ruim"),
        (1, "Insatisfeito"),
    ]

    tratamento = models.OneToOneField(
        Tratamento,
        on_delete=models.PROTECT,
        related_name="avaliacao"
    )
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    atendimento = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    infraestrutura = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    higiene = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    alimentacao = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    comunicacao = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    acolhimento = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    organizacao = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)
    gestao = models.PositiveSmallIntegerField(choices=OPCOES_AVALIACAO)

    @property
    def media(self):
        total = (
            self.atendimento +
            self.infraestrutura +
            self.higiene +
            self.alimentacao +
            self.comunicacao +
            self.acolhimento +
            self.organizacao +
            self.gestao
        )

        return total / 8

    class Meta():
        verbose_name_plural = 'avaliações'

    def __str__(self):
        return f"Avaliação - {self.paciente.nome}"


