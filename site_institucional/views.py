from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from site_institucional.forms import LoginForm
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
            "doadores": Doador.objects.all(),
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
