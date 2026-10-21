from django.urls import path
from django.contrib.auth.decorators import login_required

from painel_administrativo.permissions import administrador_required

from painel_administrativo import views


urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),

    # Centro de Formação
    path('alunos/', login_required(views.listar_alunos), name='alunos'),
    path('alunos/<int:id>/', login_required(views.detalhar_aluno), name='detalhar_aluno'),
    path('alunos/salvar/', administrador_required(views.salvar_aluno), name='salvar_aluno'),

    path('familiar/buscar-por-cpf/', login_required(views.buscar_familiar_por_cpf), name='buscar_familiar_por_cpf'),
    path('familiar/salvar/', administrador_required(views.salvar_familiar), name='salvar_familiar'),
    path('familiar/excluir/', administrador_required(views.excluir_familiar), name='excluir_familiar'),

    path('profissionais/', login_required(views.listar_profissionais), name='profissionais'),
    path('profissionais/<int:id>/', login_required(views.detalhar_profissional), name='detalhar_profissional'),
    path('profissionais/salvar/', administrador_required(views.salvar_profissional), name='salvar_profissional'),
    path('profissionais/buscar/', login_required(views.buscar_profissionais), name='buscar_profissionais'),

    path('cursos/', login_required(views.cursos), name='cursos'),
    path('turmas/', login_required(views.turmas), name='turmas'),
    path('matriculas/', login_required(views.matriculas), name='matriculas'),
    path('aulas/', login_required(views.aulas), name='aulas'),
    path('atividades/', login_required(views.atividades), name='atividades'),
    path('eventos/', login_required(views.eventos), name='eventos'),
    
    path('encontros/', login_required(views.listar_encontros), name='encontros'),
    path('encontros/<int:id>/', login_required(views.detalhar_encontro), name='detalhar_encontro'),
    path('encontros/salvar/', administrador_required(views.salvar_encontro), name='salvar_encontro'),

    path('servicos/buscar/', login_required(views.buscar_servicos), name='buscar_servicos'),

    # Casa de Apoio
    path('pacientes/', login_required(views.listar_pacientes), name='pacientes'),
    path('pacientes/<int:id>/', login_required(views.detalhar_paciente), name='detalhar_paciente'),
    path('pacientes/salvar/', administrador_required(views.salvar_paciente), name='salvar_paciente'),

    path('tratamentos/salvar/', administrador_required(views.salvar_tratamento), name='salvar_tratamento'),

    path('avaliacoes/', login_required(views.avaliacoes), name='avaliacoes'),
]
