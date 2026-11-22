from django.urls import path

from painel_administrativo import views
from painel_administrativo.views.relatorios import relatorios
from painel_administrativo.permissions import (
    acesso_painel_required,
    administrador_required,
)

urlpatterns = [
    path('', acesso_painel_required(views.dashboard), name='dashboard'),
    path('galeria/', acesso_painel_required(views.galeria), name='galeria_site'),

    # Relatórios
    path('relatorios/', acesso_painel_required(relatorios), name='relatorios'),
    path('relatorios/<slug:tipo>/', acesso_painel_required(relatorios), name='relatorio_tipo'),

    # Perfil do usuário autenticado
    path('perfil/', acesso_painel_required(views.detalhar_perfil), name='detalhar_perfil'),
    path('perfil/salvar/', acesso_painel_required(views.salvar_perfil), name='salvar_perfil'),

    # Gerenciamento de Usuários (exclusivo para administradores)
    path('usuarios/', administrador_required(views.listar_usuarios), name='usuarios'),
    path('usuarios/<int:id>/', administrador_required(views.detalhar_usuario), name='detalhar_usuario'),
    path('usuarios/salvar/', administrador_required(views.salvar_usuario), name='salvar_usuario'),
    path('usuarios/excluir/', administrador_required(views.excluir_usuario), name='excluir_usuario'),

    # Centro de Formação
    path('alunos/', acesso_painel_required(views.listar_alunos), name='alunos'),
    path('alunos/<int:id>/', acesso_painel_required(views.detalhar_aluno), name='detalhar_aluno'),
    path('alunos/salvar/', acesso_painel_required(views.salvar_aluno), name='salvar_aluno'),

    path('familiar/buscar-por-cpf/', acesso_painel_required(views.buscar_familiar_por_cpf), name='buscar_familiar_por_cpf'),
    path('familiar/salvar/', acesso_painel_required(views.salvar_familiar), name='salvar_familiar'),
    path('familiar/excluir/', acesso_painel_required(views.excluir_familiar), name='excluir_familiar'),

    path('profissionais/', acesso_painel_required(views.listar_profissionais), name='profissionais'),
    path('profissionais/<int:id>/', acesso_painel_required(views.detalhar_profissional), name='detalhar_profissional'),
    path('profissionais/salvar/', acesso_painel_required(views.salvar_profissional), name='salvar_profissional'),
    path('profissionais/buscar/', acesso_painel_required(views.buscar_profissionais), name='buscar_profissionais'),

    path('atividades/', acesso_painel_required(views.listar_atividades), name='atividades'),
    path('eventos/', acesso_painel_required(views.listar_eventos), name='eventos'),
    path('encontros/', acesso_painel_required(views.listar_encontros), name='encontros'),
    path('encontros/<int:id>/', acesso_painel_required(views.detalhar_encontro), name='detalhar_encontro'),
    path('encontros/salvar/', acesso_painel_required(views.salvar_encontro), name='salvar_encontro'),

    path('cursos/', acesso_painel_required(views.listar_cursos), name='cursos'),
    path('turmas/', acesso_painel_required(views.listar_turmas), name='turmas'),
    path('turmas/<int:id>/', acesso_painel_required(views.detalhar_turma), name='detalhar_turma'),
    path('turmas/salvar/', acesso_painel_required(views.salvar_turma), name='salvar_turma'),
    path('turmas/buscar-alunos-nao-matriculados/<int:turma_id>/', acesso_painel_required(views.buscar_alunos_nao_matriculados_na_turma), name='buscar_alunos_nao_matriculados'),
    path('turmas/buscar-alunos-matriculados/<int:turma_id>/', acesso_painel_required(views.buscar_alunos_matriculados_na_turma), name='buscar_alunos_matriculados'),

    path('matriculas/salvar/', acesso_painel_required(views.salvar_matricula), name='salvar_matricula'),
    path('matriculas/excluir/', acesso_painel_required(views.excluir_matricula), name='excluir_matricula'),

    path('aulas/buscar_frequencias/<int:aula_id>/', acesso_painel_required(views.buscar_frequencias), name='buscar_frequencias'),
    path('aulas/salvar/', acesso_painel_required(views.salvar_aula), name='salvar_aula'),
    path('aulas/excluir/', acesso_painel_required(views.excluir_aula), name='excluir_aula'),

    path('servicos/buscar/', acesso_painel_required(views.buscar_servicos), name='buscar_servicos'),
    path('servicos/<int:id>/', acesso_painel_required(views.detalhar_servico), name='detalhar_servico'),
    path('servicos/salvar/', acesso_painel_required(views.salvar_servico), name='salvar_servico'),

    # Casa de Apoio
    path('pacientes/', acesso_painel_required(views.listar_pacientes), name='pacientes'),
    path('pacientes/<int:id>/', acesso_painel_required(views.detalhar_paciente), name='detalhar_paciente'),
    path('pacientes/salvar/', acesso_painel_required(views.salvar_paciente), name='salvar_paciente'),

    path('tratamentos/salvar/', acesso_painel_required(views.salvar_tratamento), name='salvar_tratamento'),
]
