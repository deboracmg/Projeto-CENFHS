from django.contrib import admin

from painel_administrativo.models.pessoas import Aluno, Profissional, Saude, Socioeconomico, Parente, Parentesco, Paciente
from painel_administrativo.models.servicos import Aula, Encontro, Frequencia, Matricula, Servico, Turma, Avaliacao, Tratamento

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Profissional)
admin.site.register(Saude)
admin.site.register(Socioeconomico)
admin.site.register(Parente)
admin.site.register(Parentesco)
admin.site.register(Paciente)

admin.site.register(Servico)
admin.site.register(Turma)
admin.site.register(Matricula)
admin.site.register(Aula)
admin.site.register(Frequencia)
admin.site.register(Encontro)
admin.site.register(Tratamento)
admin.site.register(Avaliacao)

