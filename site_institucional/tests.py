import json
import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class ControleDeAcessoEAutenticacaoTests(TestCase):
    password = "Senha-forte-123!"

    def criar_usuario(self, primeiro_acesso=False, **kwargs):
        dados = {
            "username": "colaborador",
            "first_name": "Colaborador Teste",
            "email": "colaborador@example.com",
            "last_login": None if primeiro_acesso else timezone.now(),
        }
        dados.update(kwargs)
        return User.objects.create_user(password=self.password, **dados)

    def criar_administrador(self, **kwargs):
        dados = {
            "username": "admin",
            "first_name": "Administrador",
            "email": "admin@example.com",
            "is_staff": True,
            "last_login": timezone.now(),
        }
        dados.update(kwargs)
        return User.objects.create_user(password=self.password, **dados)

    def test_paginas_publicas_acessiveis_sem_login(self):
        for rota in ("index", "our_services", "contact_us", "login", "password_reset"):
            with self.subTest(rota=rota):
                response = self.client.get(reverse(rota))
                self.assertEqual(response.status_code, 200)

    def test_todas_rotas_do_dashboard_exigem_autenticacao(self):
        rotas_get = [
            ("dashboard", ()),
            ("galeria_site", ()),
            ("detalhar_perfil", ()),
            ("usuarios", ()),
            ("detalhar_usuario", (1,)),
            ("alunos", ()),
            ("detalhar_aluno", (1,)),
            ("buscar_familiar_por_cpf", ()),
            ("profissionais", ()),
            ("detalhar_profissional", (1,)),
            ("buscar_profissionais", ()),
            ("atividades", ()),
            ("eventos", ()),
            ("encontros", ()),
            ("detalhar_encontro", (1,)),
            ("cursos", ()),
            ("turmas", ()),
            ("detalhar_turma", (1,)),
            ("buscar_alunos_nao_matriculados", (1,)),
            ("buscar_alunos_matriculados", (1,)),
            ("buscar_frequencias", (1,)),
            ("buscar_servicos", ()),
            ("detalhar_servico", (1,)),
            ("pacientes", ()),
            ("detalhar_paciente", (1,)),
        ]
        for nome, args in rotas_get:
            with self.subTest(rota=nome, metodo="GET"):
                response = self.client.get(reverse(nome, args=args))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response.url)

        rotas_post = [
            "salvar_perfil",
            "salvar_usuario",
            "excluir_usuario",
            "salvar_aluno",
            "salvar_familiar",
            "excluir_familiar",
            "salvar_profissional",
            "salvar_encontro",
            "salvar_turma",
            "salvar_matricula",
            "excluir_matricula",
            "salvar_aula",
            "excluir_aula",
            "salvar_servico",
            "salvar_paciente",
            "salvar_tratamento",
        ]
        for nome in rotas_post:
            with self.subTest(rota=nome, metodo="POST"):
                response = self.client.post(reverse(nome), {})
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response.url)

    def test_login_autentica_usuario_ativo_com_acesso_previo(self):
        self.criar_usuario(primeiro_acesso=False)
        response = self.client.post(
            reverse("login"),
            {"username": "colaborador", "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_rejeita_senha_incorreta_e_usuario_inativo(self):
        usuario = self.criar_usuario()
        response = self.client.post(
            reverse("login"),
            {"username": "colaborador", "password": "senha-errada"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

        usuario.is_active = False
        usuario.save()
        response_inativo = self.client.post(
            reverse("login"),
            {"username": "colaborador", "password": self.password},
        )
        self.assertEqual(response_inativo.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_primeiro_acesso_exige_troca_de_senha_temporaria(self):
        usuario = self.criar_usuario(primeiro_acesso=True)
        response = self.client.post(
            reverse("login"),
            {"username": "colaborador", "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("alterar_senha_obrigatoria"))

        usuario.refresh_from_db()
        self.assertIsNone(usuario.last_login)

        # Tentativa de acessar o dashboard antes de trocar a senha temporária é bloqueada
        resp_painel = self.client.get(reverse("dashboard"))
        self.assertEqual(resp_painel.status_code, 302)
        self.assertEqual(resp_painel.url, reverse("alterar_senha_obrigatoria"))

        # Rejeita repetir a mesma senha temporária
        resp_mesma_senha = self.client.post(
            reverse("alterar_senha_obrigatoria"),
            {
                "new_password1": self.password,
                "new_password2": self.password,
            },
        )
        self.assertEqual(resp_mesma_senha.status_code, 200)
        usuario.refresh_from_db()
        self.assertIsNone(usuario.last_login)

        # Aceita nova senha válida e libera o acesso ao dashboard
        nova_senha = "Nova-Senha-Forte-456!"
        resp_troca = self.client.post(
            reverse("alterar_senha_obrigatoria"),
            {
                "new_password1": nova_senha,
                "new_password2": nova_senha,
            },
        )
        self.assertEqual(resp_troca.status_code, 302)
        self.assertEqual(resp_troca.url, reverse("dashboard"))

        usuario.refresh_from_db()
        self.assertIsNotNone(usuario.last_login)
        self.assertTrue(usuario.check_password(nova_senha))

        resp_painel_liberado = self.client.get(reverse("dashboard"))
        self.assertEqual(resp_painel_liberado.status_code, 200)

    def test_usuario_comum_nao_pode_gerenciar_usuarios(self):
        outro = self.criar_usuario(username="outro", email="outro@example.com")
        self.criar_usuario()
        self.client.login(username="colaborador", password=self.password)

        self.assertEqual(self.client.get(reverse("usuarios")).status_code, 403)
        self.assertEqual(
            self.client.get(reverse("detalhar_usuario", args=[outro.id])).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("salvar_usuario"),
                {
                    "nome": "Invasor",
                    "username": "invasor",
                    "email": "invasor@example.com",
                    "senha": self.password,
                    "confirmar_senha": self.password,
                },
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(
                reverse("excluir_usuario"),
                data=json.dumps({"usuario_id": outro.id}),
                content_type="application/json",
            ).status_code,
            403,
        )

    def test_administrador_executa_crud_de_usuarios_e_redefine_senha_temporaria(self):
        admin = self.criar_administrador(username="admin.logado")
        self.client.login(username="admin.logado", password=self.password)

        # Cadastro de novo usuário com senha temporária gerada
        resp_criar = self.client.post(
            reverse("salvar_usuario"),
            {
                "nome": "Maria Colaboradora",
                "username": "maria.colab",
                "email": "maria@example.com",
                "senha": "Temp-Password-999!",
                "ativo": "on",
            },
        )
        self.assertEqual(resp_criar.status_code, 200)
        novo_usuario = User.objects.get(username="maria.colab")
        self.assertFalse(novo_usuario.is_staff)
        self.assertIsNone(novo_usuario.last_login)
        self.assertNotEqual(novo_usuario.password, "Temp-Password-999!")
        self.assertTrue(novo_usuario.check_password("Temp-Password-999!"))

        # Listagem exibe o outro usuário, mas oculta o próprio administrador autenticado
        resp_lista = self.client.get(reverse("usuarios"))
        self.assertEqual(resp_lista.status_code, 200)
        self.assertContains(resp_lista, "maria.colab")
        self.assertNotContains(resp_lista, "<td>admin.logado</td>", html=True)

        # Simula que o usuário já havia acessado antes e depois o admin redefine senha temporária
        novo_usuario.last_login = timezone.now()
        novo_usuario.save(update_fields=["last_login"])

        resp_reset = self.client.post(
            reverse("salvar_usuario"),
            {
                "usuario_id": novo_usuario.id,
                "nome": "Maria Colaboradora",
                "username": "maria.colab",
                "email": "maria@example.com",
                "senha": "Outra-Temp-Password-888!",
                "ativo": "on",
            },
        )
        self.assertEqual(resp_reset.status_code, 200)
        novo_usuario.refresh_from_db()
        self.assertIsNone(novo_usuario.last_login)
        self.assertTrue(novo_usuario.check_password("Outra-Temp-Password-888!"))

        # Administrador não pode detalhar, editar, definir senha temporária ou excluir a própria conta por esta tela
        self.assertEqual(
            self.client.get(reverse("detalhar_usuario", args=[admin.id])).status_code,
            400,
        )
        resp_auto_editar = self.client.post(
            reverse("salvar_usuario"),
            {
                "usuario_id": admin.id,
                "nome": "Administrador",
                "username": "admin.logado",
                "email": "admin@example.com",
                "senha": "Temp-Propria-123!",
                "is_staff": "on",
                "ativo": "on",
            },
        )
        self.assertEqual(resp_auto_editar.status_code, 400)

        resp_auto_excluir = self.client.delete(
            reverse("excluir_usuario"),
            data=json.dumps({"usuario_id": admin.id}),
            content_type="application/json",
        )
        self.assertEqual(resp_auto_excluir.status_code, 400)

        # Exclusão de outro usuário
        resp_excluir = self.client.delete(
            reverse("excluir_usuario"),
            data=json.dumps({"usuario_id": novo_usuario.id}),
            content_type="application/json",
        )
        self.assertEqual(resp_excluir.status_code, 200)
        self.assertFalse(User.objects.filter(id=novo_usuario.id).exists())

    def test_usuario_comum_edita_perfil_mas_nao_pode_virar_administrador(self):
        usuario = self.criar_usuario()
        self.client.login(username="colaborador", password=self.password)

        response = self.client.post(
            reverse("salvar_perfil"),
            {
                "nome": "João Pedro Silva",
                "username": "colaborador.novo",
                "email": "novo@example.com",
                "is_staff": "on",
                "is_superuser": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["saudacao"], "João")

        usuario.refresh_from_db()
        self.assertEqual(usuario.first_name, "João Pedro Silva")
        self.assertEqual(usuario.username, "colaborador.novo")
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

        resp_painel = self.client.get(reverse("dashboard"))
        self.assertContains(resp_painel, "Olá, João!")

    def test_alteracao_de_senha_no_perfil_exige_senha_atual_correta(self):
        usuario = self.criar_usuario()
        self.client.login(username="colaborador", password=self.password)

        resp_erro = self.client.post(
            reverse("salvar_perfil"),
            {
                "nome": "Colaborador",
                "username": "colaborador",
                "email": "colaborador@example.com",
                "senha_atual": "senha-errada",
                "nova_senha": "Nova-Senha-Segura-789!",
                "confirmar_nova_senha": "Nova-Senha-Segura-789!",
            },
        )
        self.assertEqual(resp_erro.status_code, 400)

        resp_ok = self.client.post(
            reverse("salvar_perfil"),
            {
                "nome": "Colaborador",
                "username": "colaborador",
                "email": "colaborador@example.com",
                "senha_atual": self.password,
                "nova_senha": "Nova-Senha-Segura-789!",
                "confirmar_nova_senha": "Nova-Senha-Segura-789!",
            },
        )
        self.assertEqual(resp_ok.status_code, 200)
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password("Nova-Senha-Segura-789!"))
        self.assertIn("_auth_user_id", self.client.session)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_recuperacao_de_senha_por_email_restrita_a_administradores(self):
        self.criar_usuario(email="comum@example.com")
        admin = self.criar_administrador(email="admin@example.com")

        # Usuário comum não recebe e-mail de redefinição
        resp_comum = self.client.post(
            reverse("password_reset"),
            {"email": "comum@example.com"},
        )
        self.assertEqual(resp_comum.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

        # Administrador ativo recebe e-mail e consegue redefinir a senha
        resp_admin = self.client.post(
            reverse("password_reset"),
            {"email": "admin@example.com"},
        )
        self.assertEqual(resp_admin.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        match = re.search(
            r"/redefinir-senha/(?P<uidb64>[^/]+)/(?P<token>[^/\s]+)/",
            mail.outbox[0].body,
        )
        self.assertIsNotNone(match)

        url_confirm = reverse(
            "password_reset_confirm",
            kwargs=match.groupdict(),
        )
        resp_follow = self.client.get(url_confirm)
        self.assertEqual(resp_follow.status_code, 302)

        resp_redefinir = self.client.post(
            resp_follow.url,
            {
                "new_password1": "Admin-Nova-Senha-321!",
                "new_password2": "Admin-Nova-Senha-321!",
            },
        )
        self.assertEqual(resp_redefinir.status_code, 302)
        self.assertEqual(resp_redefinir.url, reverse("password_reset_complete"))

        admin.refresh_from_db()
        self.assertTrue(admin.check_password("Admin-Nova-Senha-321!"))

    def test_logout_exige_post_e_encerra_sessao(self):
        self.criar_usuario()
        self.client.login(username="colaborador", password=self.password)
        response_get = self.client.get(reverse("logout"))
        self.assertEqual(response_get.status_code, 405)
        response_post = self.client.post(reverse("logout"))
        self.assertEqual(response_post.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_post_sem_token_csrf_e_bloqueado(self):
        cliente = Client(enforce_csrf_checks=True)
        response = cliente.post(reverse("about_us"), {"nome": "Teste", "valor": "10,00"})
        self.assertEqual(response.status_code, 403)

    def test_senhas_sao_armazenadas_com_hash(self):
        usuario = self.criar_usuario()
        self.assertNotEqual(usuario.password, self.password)
        self.assertTrue(usuario.password.startswith("pbkdf2_"))
        self.assertTrue(usuario.check_password(self.password))
