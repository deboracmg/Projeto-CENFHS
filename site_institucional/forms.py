from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils import timezone


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


class RecuperarSenhaAdminForm(PasswordResetForm):
    """Permite recuperação de senha por e-mail exclusivamente para administradores."""

    # TODO: implementar envio de email de recuperação de senha com configuração SMTP

    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Seu e-mail cadastrado",
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
    )

    def get_users(self, email):
        usuarios = super().get_users(email)
        return (
            usuario
            for usuario in usuarios
            if usuario.is_staff or usuario.is_superuser
        )


class DefinirNovaSenhaForm(SetPasswordForm):
    """Formulário para definição de nova senha com rótulos em português."""

    new_password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Digite a nova senha",
                "autocomplete": "new-password",
                "autofocus": True,
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repita a nova senha",
                "autocomplete": "new-password",
            }
        ),
    )


class PrimeiroAcessoSenhaForm(DefinirNovaSenhaForm):
    """Exige que o usuário substitua a senha temporária por uma nova senha diferente."""

    def clean_new_password1(self):
        senha = self.cleaned_data.get("new_password1")
        if senha and self.user.check_password(senha):
            raise forms.ValidationError(
                "A nova senha deve ser diferente da senha temporária."
            )
        return senha

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.last_login = timezone.now()
        if commit:
            self.user.save(update_fields=["password", "last_login"])
        return self.user
