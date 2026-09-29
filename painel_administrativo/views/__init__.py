from django.shortcuts import render

from .alunos import listar_alunos, detalhar_aluno, salvar_aluno
from .parentes import buscar_parente, detalhar_parente, salvar_parente
from .profissionais import listar_profissionais, listar_pacientes
from .servicos import cursos, turmas, aulas, matriculas, atividades, eventos, encontros, avaliacoes


def dashboard(request):
    return render(
        request,
        'painel/dashboard.html'
    )

