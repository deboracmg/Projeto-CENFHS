from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def administrador_required(view_func):
    """Restringe alterações administrativas a usuários staff/superusuários."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="login")
        if not (user.is_staff or user.is_superuser):
            raise PermissionDenied("Você não tem permissão para executar esta ação.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
