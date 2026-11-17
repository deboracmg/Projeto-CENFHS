from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from painel_administrativo.permissions import _precisa_alterar_senha_temporaria
from site_institucional.forms import (
    DefinirNovaSenhaForm,
    LoginForm,
    PrimeiroAcessoSenhaForm,
)
from site_institucional.models import Doador

# TODO: estas listas ainda são estáticas. Quando o painel administrativo
# passar a alimentar o site, troque por consultas aos modelos de
# painel_administrativo (Servico, Turma, Encontro etc.).
PROXIMOS_EVENTOS = []

ATIVIDADES = []


def _parse_valor(bruto):
    """Converte um valor digitado (ex.: 'R$ 1.234,56') para float, ou None se inválido."""
    if not bruto:
        return None

    limpo = bruto.replace("R$", "").strip()
    if "," in limpo and "." in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    else:
        limpo = limpo.replace(",", ".")

    try:
        valor = float(limpo)
    except ValueError:
        return None

    return valor if valor > 0 else None


def index(request):
    return render(
        request,
        "site/index.html",
        {
            "active_page": "index",
            "proximos_eventos": PROXIMOS_EVENTOS,
        },
    )


def about_us(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()[:120]
        valor = _parse_valor(request.POST.get("valor", ""))

        if nome:
            Doador.objects.create(nome=nome, valor=valor)
            return redirect(f"{reverse('about_us')}?doado=1&nome={quote(nome)}#doacoes")

        return redirect(f"{reverse('about_us')}#doacoes")

    return render(
        request,
        "site/about-us.html",
        {
            "active_page": "about_us",
            "doadores": Doador.objects.filter(aprovado=True),
            "doacao_concluida": request.GET.get("doado") == "1",
            "doador_nome": request.GET.get("nome", ""),
        },
    )


def our_services(request):
    return render(
        request,
        "site/our-services.html",
        {
            "active_page": "our_services",
            "proximos_eventos": PROXIMOS_EVENTOS,
            "atividades": ATIVIDADES,
            "atividades_total_inicio": 1 if ATIVIDADES else 0,
            "atividades_total_fim": len(ATIVIDADES),
        },
    )


def contact_us(request):
    if request.method == "POST":
        messages.success(request, "Mensagem enviada com sucesso! Em breve entraremos em contato.")
        return redirect("contact_us")

    return render(
        request,
        "site/contact-us.html",
        {
            "active_page": "contact_us",
        },
    )


class EntrarView(LoginView):
    """Página de entrada da equipe (login), no mesmo visual do site."""

    template_name = "site/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    extra_context = {"active_page": "login"}

    def form_valid(self, form):
        usuario = form.get_user()
        exige_troca_senha = (
            not (usuario.is_staff or usuario.is_superuser)
            and usuario.last_login is None
        )
        response = super().form_valid(form)
        if exige_troca_senha:
            usuario.last_login = None
            usuario.save(update_fields=["last_login"])
            self.request.session["forcar_troca_senha"] = True
            return redirect("alterar_senha_obrigatoria")
        self.request.session.pop("forcar_troca_senha", None)
        return response

    def get_success_url(self):
        if _precisa_alterar_senha_temporaria(self.request):
            return reverse("alterar_senha_obrigatoria")
        return super().get_success_url()


class RedefinirSenhaAdminConfirmView(PasswordResetConfirmView):
    """Redefinição de senha por token para administradores."""

    template_name = "site/password_reset_confirm.html"
    form_class = DefinirNovaSenhaForm
    success_url = reverse_lazy("password_reset_complete")
    extra_context = {"active_page": "login"}

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.user and self.user.last_login is None:
            self.user.last_login = timezone.now()
            self.user.save(update_fields=["last_login"])
        return response


@login_required
@require_http_methods(["GET", "POST"])
def alterar_senha_obrigatoria(request):
    """Exige que o usuário substitua sua senha temporária antes de acessar o painel."""
    if not _precisa_alterar_senha_temporaria(request):
        return redirect("dashboard")

    if request.method == "POST":
        form = PrimeiroAcessoSenhaForm(request.user, request.POST)
        if form.is_valid():
            usuario = form.save()
            request.session.pop("forcar_troca_senha", None)
            update_session_auth_hash(request, usuario)
            return redirect("dashboard")
    else:
        form = PrimeiroAcessoSenhaForm(request.user)

    return render(
        request,
        "site/password_first_access.html",
        {
            "form": form,
            "active_page": "login",
        },
    )
