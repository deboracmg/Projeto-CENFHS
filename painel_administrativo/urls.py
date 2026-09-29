from django.urls import path

from painel_administrativo import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Centro de Formação
    path('alunos/', views.listar_alunos, name='alunos'),
    path('alunos/<int:id>/', views.detalhar_aluno, name='detalhar_aluno'),
    path('alunos/salvar/', views.salvar_aluno, name='salvar_aluno'),

    path('parentes/<int:parente_id>/', views.detalhar_parente, name='detalhar_parente'),
    # path('parentes/buscar/', views.buscar_parente, name='buscar_parente'),
    path('parentes/salvar/', views.salvar_parente, name='salvar_parente'),


    path('profissionais/', views.listar_profissionais, name='profissionais'),
    path('cursos/', views.cursos, name='cursos'),
    path('turmas/', views.turmas, name='turmas'),
    path('matriculas/', views.matriculas, name='matriculas'),
    path('aulas/', views.aulas, name='aulas'),
    path('atividades/', views.atividades, name='atividades'),
    path('eventos/', views.eventos, name='eventos'),
    path('encontros/', views.encontros, name='encontros'),


    # Casa de Apoio
    path('pacientes/', views.listar_pacientes, name='pacientes'),
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
]
