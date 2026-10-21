from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


class ControleDeAcessoTests(TestCase):
    password = 'Senha-forte-123!'

    def criar_usuario(self, **kwargs):
        dados = {'username': 'colaborador', 'email': 'colaborador@example.com'}
        dados.update(kwargs)
        return User.objects.create_user(password=self.password, **dados)

    def test_dashboard_redireciona_usuario_nao_autenticado(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_rotas_do_dashboard_exigem_autenticacao(self):
        rotas = [
            ('dashboard', ()), ('alunos', ()), ('profissionais', ()),
            ('cursos', ()), ('turmas', ()), ('matriculas', ()), ('aulas', ()),
            ('atividades', ()), ('eventos', ()), ('encontros', ()),
            ('pacientes', ()), ('avaliacoes', ()), ('buscar_servicos', ()),
            ('buscar_profissionais', ()), ('buscar_familiar_por_cpf', ()),
        ]
        for nome, args in rotas:
            with self.subTest(rota=nome):
                response = self.client.get(reverse(nome, args=args))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse('login'), response.url)

    def test_login_autentica_usuario_ativo(self):
        self.criar_usuario()
        response = self.client.post(reverse('login'), {
            'username': 'colaborador', 'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_rejeita_senha_incorreta(self):
        self.criar_usuario()
        response = self.client.post(reverse('login'), {
            'username': 'colaborador', 'password': 'senha-errada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_usuario_comum_nao_pode_executar_acoes_administrativas(self):
        self.criar_usuario()
        self.client.login(username='colaborador', password=self.password)
        for nome in ('salvar_aluno', 'salvar_familiar', 'excluir_familiar',
                     'salvar_profissional', 'salvar_encontro', 'salvar_paciente',
                     'salvar_tratamento'):
            with self.subTest(rota=nome):
                response = self.client.post(reverse(nome), {})
                self.assertEqual(response.status_code, 403)

    def test_administrador_pode_acessar_rota_de_cadastro(self):
        User.objects.create_superuser(
            username='admin', email='admin@example.com', password=self.password
        )
        self.client.login(username='admin', password=self.password)
        response = self.client.post(reverse('salvar_aluno'), {})
        self.assertNotEqual(response.status_code, 403)

    def test_logout_exige_post_e_encerra_sessao(self):
        self.criar_usuario()
        self.client.login(username='colaborador', password=self.password)
        response_get = self.client.get(reverse('logout'))
        self.assertEqual(response_get.status_code, 405)
        response_post = self.client.post(reverse('logout'))
        self.assertEqual(response_post.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_recuperacao_de_senha_exibe_formulario(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_post_sem_token_csrf_e_bloqueado(self):
        from django.test import Client
        cliente = Client(enforce_csrf_checks=True)
        response = cliente.post(reverse('about_us'), {'nome': 'Teste', 'valor': '10,00'})
        self.assertEqual(response.status_code, 403)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_recuperacao_de_senha_envia_email_para_conta_existente(self):
        self.criar_usuario()
        response = self.client.post(reverse('password_reset'), {'email': 'colaborador@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('redefinir-senha/', mail.outbox[0].body)

    def test_senhas_sao_armazenadas_com_hash(self):
        usuario = self.criar_usuario()
        self.assertNotEqual(usuario.password, self.password)
        self.assertTrue(usuario.check_password(self.password))
