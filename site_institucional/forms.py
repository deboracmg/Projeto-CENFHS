from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Formulário de entrada da equipe, com rótulos e dicas em português."""

    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Seu usuário",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Sua senha",
                "autocomplete": "current-password",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Usuário ou senha incorretos. Confira os dados e tente novamente.",
        "inactive": "Esta conta está desativada.",
    }
