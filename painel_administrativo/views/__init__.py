from django.shortcuts import render

from .alunos import listar_alunos, detalhar_aluno, salvar_aluno
from .parentes import buscar_parente_por_cpf, salvar_parente, excluir_parente
from .profissionais import listar_profissionais, detalhar_profissional, salvar_profissional
from .pacientes import listar_pacientes, detalhar_paciente, salvar_paciente
from .servicos import cursos, turmas, aulas, matriculas, atividades, eventos, encontros, avaliacoes


def dashboard(request):
    return render(
        request,
        'painel/dashboard.html'
    )

