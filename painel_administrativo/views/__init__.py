from django.shortcuts import render

from .alunos import listar_alunos, detalhar_aluno, salvar_aluno
from .familia import buscar_familiar_por_cpf, salvar_familiar, excluir_familiar
from .tratamentos import salvar_tratamento
from .profissionais import listar_profissionais, detalhar_profissional, buscar_profissionais, salvar_profissional
from .pacientes import listar_pacientes, detalhar_paciente, salvar_paciente
from .servicos import buscar_servicos, cursos, turmas, aulas, matriculas, atividades, eventos, avaliacoes
from .encontros import listar_encontros, detalhar_encontro, salvar_encontro


def dashboard(request):
    return render(
        request,
        'painel/dashboard.html'
    )

