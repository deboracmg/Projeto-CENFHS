from django.urls import path

from painel_administrativo import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Centro de Formação
    path('alunos/', views.listar_alunos, name='alunos'),
    path('alunos/<int:id>/', views.detalhar_aluno, name='detalhar_aluno'),
    path('alunos/salvar/', views.salvar_aluno, name='salvar_aluno'),

    path('familiar/buscar-por-cpf/', views.buscar_familiar_por_cpf, name='buscar_familiar_por_cpf'),
    path('familiar/salvar/', views.salvar_familiar, name='salvar_familiar'),
    path('familiar/excluir/', views.excluir_familiar, name='excluir_familiar'),

    path('profissionais/', views.listar_profissionais, name='profissionais'),
    path('profissionais/<int:id>/', views.detalhar_profissional, name='detalhar_profissional'),
    path('profissionais/salvar/', views.salvar_profissional, name='salvar_profissional'),
    path('profissionais/buscar/', views.buscar_profissionais, name='buscar_profissionais'),
 
    path('atividades/', views.listar_atividades, name='atividades'),
    path('eventos/', views.listar_eventos, name='eventos'),
    path('encontros/', views.listar_encontros, name='encontros'),
    path('encontros/<int:id>/', views.detalhar_encontro, name='detalhar_encontro'),
    path('encontros/salvar/', views.salvar_encontro, name='salvar_encontro'),

    path('cursos/', views.listar_cursos, name='cursos'),
    path('turmas/', views.listar_turmas, name='turmas'),
    path('turmas/<int:id>', views.detalhar_turma, name='detalhar_turma'),
    path('turmas/salvar/', views.salvar_turma, name='salvar_turma'),

    path('matriculas/', views.matriculas, name='matriculas'),
    path('aulas/', views.aulas, name='aulas'),

    path('servicos/buscar/', views.buscar_servicos, name='buscar_servicos'),
    path('servicos/<int:id>/', views.detalhar_servico, name='detalhar_servico'),
    path('servicos/salvar/', views.salvar_servico, name='salvar_servico'),

    # Casa de Apoio
    path('pacientes/', views.listar_pacientes, name='pacientes'),
    path('pacientes/<int:id>/', views.detalhar_paciente, name='detalhar_paciente'),
    path('pacientes/salvar/', views.salvar_paciente, name='salvar_paciente'),

    path('tratamentos/salvar/', views.salvar_tratamento, name='salvar_tratamento'),
]
