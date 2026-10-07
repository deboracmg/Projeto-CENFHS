from django.urls import path

from painel_administrativo import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Centro de Formação
    path('alunos/', views.listar_alunos, name='alunos'),
    path('alunos/<int:id>/', views.detalhar_aluno, name='detalhar_aluno'),
    path('alunos/salvar/', views.salvar_aluno, name='salvar_aluno'),

    path('parentes/buscar-por-cpf/', views.buscar_parente_por_cpf, name='buscar_parente_por_cpf'),
    path('parentes/salvar/', views.salvar_parente, name='salvar_parente'),
    path('parentes/excluir/', views.excluir_parente, name='excluir_parente'),

    path('profissionais/', views.listar_profissionais, name='profissionais'),
    path('profissionais/<int:id>/', views.detalhar_profissional, name='detalhar_profissional'),
    path('profissionais/salvar/', views.salvar_profissional, name='salvar_profissional'),

    path('cursos/', views.cursos, name='cursos'),
    path('turmas/', views.turmas, name='turmas'),
    path('matriculas/', views.matriculas, name='matriculas'),
    path('aulas/', views.aulas, name='aulas'),
    path('atividades/', views.atividades, name='atividades'),
    path('eventos/', views.eventos, name='eventos'),
    path('encontros/', views.encontros, name='encontros'),


    # Casa de Apoio
    path('pacientes/', views.listar_pacientes, name='pacientes'),
    path('pacientes/<int:id>/', views.detalhar_paciente, name='detalhar_paciente'),
    path('pacientes/salvar/', views.salvar_paciente, name='salvar_paciente'),

    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
]
