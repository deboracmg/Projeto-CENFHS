from django.urls import path
from django.contrib.auth.decorators import login_required

from painel_administrativo import views

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('galeria/', login_required(views.galeria), name='galeria_site'),

    # Centro de Formação
    path('alunos/', login_required(views.listar_alunos), name='alunos'),
    path('alunos/<int:id>/', login_required(views.detalhar_aluno), name='detalhar_aluno'),
    path('alunos/salvar/', login_required(views.salvar_aluno), name='salvar_aluno'),

    path('familiar/buscar-por-cpf/', login_required(views.buscar_familiar_por_cpf), name='buscar_familiar_por_cpf'),
    path('familiar/salvar/', login_required(views.salvar_familiar), name='salvar_familiar'),
    path('familiar/excluir/', login_required(views.excluir_familiar), name='excluir_familiar'),

    path('profissionais/', login_required(views.listar_profissionais), name='profissionais'),
    path('profissionais/<int:id>/', login_required(views.detalhar_profissional), name='detalhar_profissional'),
    path('profissionais/salvar/', login_required(views.salvar_profissional), name='salvar_profissional'),
    path('profissionais/buscar/', login_required(views.buscar_profissionais), name='buscar_profissionais'),
 
    path('atividades/', login_required(views.listar_atividades), name='atividades'),
    path('eventos/', login_required(views.listar_eventos), name='eventos'),
    path('encontros/', login_required(views.listar_encontros), name='encontros'),
    path('encontros/<int:id>/', login_required(views.detalhar_encontro), name='detalhar_encontro'),
    path('encontros/salvar/', login_required(views.salvar_encontro), name='salvar_encontro'),

    path('cursos/', login_required(views.listar_cursos), name='cursos'),
    path('turmas/', login_required(views.listar_turmas), name='turmas'),
    path('turmas/<int:id>/', login_required(views.detalhar_turma), name='detalhar_turma'),
    path('turmas/salvar/', login_required(views.salvar_turma), name='salvar_turma'),
    path('turmas/buscar-alunos-nao-matriculados/<int:turma_id>/', login_required(views.buscar_alunos_nao_matriculados_na_turma), name='buscar_alunos_nao_matriculados'),
    path('turmas/buscar-alunos-matriculados/<int:turma_id>/', login_required(views.buscar_alunos_matriculados_na_turma), name='buscar_alunos_matriculados'),

    path('matriculas/salvar/', login_required(views.salvar_matricula), name='salvar_matricula'),
    path('matriculas/excluir/', login_required(views.excluir_matricula), name='excluir_matricula'),
    
    path('aulas/buscar_frequencias/<int:aula_id>/', login_required(views.buscar_frequencias), name='buscar_frequencias'),
    path('aulas/salvar/', login_required(views.salvar_aula), name='salvar_aula'),
    path("aulas/excluir/", login_required(views.excluir_aula), name="excluir_aula"),

    path('servicos/buscar/', login_required(views.buscar_servicos), name='buscar_servicos'),
    path('servicos/<int:id>/', login_required(views.detalhar_servico), name='detalhar_servico'),
    path('servicos/salvar/', login_required(views.salvar_servico), name='salvar_servico'),

    # Casa de Apoio
    path('pacientes/', login_required(views.listar_pacientes), name='pacientes'),
    path('pacientes/<int:id>/', login_required(views.detalhar_paciente), name='detalhar_paciente'),
    path('pacientes/salvar/', login_required(views.salvar_paciente), name='salvar_paciente'),

    path('tratamentos/salvar/', login_required(views.salvar_tratamento), name='salvar_tratamento'),
]
