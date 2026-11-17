from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect


def _precisa_alterar_senha_temporaria(request):
    user = request.user
    if not user.is_authenticated:
        return False
    if request.session.get("forcar_troca_senha"):
        return True
    if not (user.is_staff or user.is_superuser) and user.last_login is None:
        return True
    return False


def acesso_painel_required(view_func):
    """Exige usuário autenticado e sem pendência de troca obrigatória de senha."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="login")
        if _precisa_alterar_senha_temporaria(request):
            return redirect("alterar_senha_obrigatoria")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def administrador_required(view_func):
    """Restringe o gerenciamento de usuários exclusivamente a administradores."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="login")
        if _precisa_alterar_senha_temporaria(request):
            return redirect("alterar_senha_obrigatoria")
        if not (user.is_staff or user.is_superuser):
            if request.method != "GET":
                return JsonResponse(
                    {
                        "sucesso": False,
                        "mensagem": "Você não tem permissão para executar esta ação.",
                    },
                    status=403,
                )
            raise PermissionDenied("Você não tem permissão para executar esta ação.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
