from django.shortcuts import render

from .alunos import listar_alunos, detalhar_aluno, salvar_aluno
from .familia import buscar_familiar_por_cpf, salvar_familiar, excluir_familiar
from .tratamentos import salvar_tratamento
from .profissionais import listar_profissionais, detalhar_profissional, buscar_profissionais, salvar_profissional
from .pacientes import listar_pacientes, detalhar_paciente, salvar_paciente
from .servicos import buscar_servicos, detalhar_servico, salvar_servico, listar_cursos, listar_atividades, listar_eventos
from .turmas import listar_turmas, detalhar_turma, buscar_alunos_nao_matriculados_na_turma, buscar_alunos_matriculados_na_turma, salvar_turma
from .matriculas import buscar_matriculas, excluir_matricula, salvar_matricula
from .aulas import buscar_aulas, buscar_frequencias, salvar_aula, excluir_aula
from .encontros import listar_encontros, detalhar_encontro, salvar_encontro


def dashboard(request):
    return render(
        request,
        'painel/dashboard.html'
    )

