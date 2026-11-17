import json

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

User = get_user_model()


def listar_usuarios(request):
    usuarios = (
        User.objects.exclude(id=request.user.id)
        .order_by("-date_joined", "-id")
    )
    return render(
        request,
        "painel/pessoas/usuarios.html",
        {"usuarios": usuarios},
    )


def detalhar_usuario(request, id):
    if request.method != "GET":
        return JsonResponse(
            {"sucesso": False, "mensagem": "Método não permitido."},
            status=405,
        )

    if int(id) == request.user.id:
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Utilize a opção 'Meu perfil' para gerenciar sua própria conta.",
            },
            status=400,
        )

    try:
        usuario = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Usuário não encontrado."},
            status=404,
        )

    dados = {
        "usuario_id": usuario.id,
        "username": usuario.username,
        "nome": usuario.first_name,
        "email": usuario.email,
        "is_staff": bool(usuario.is_staff or usuario.is_superuser),
        "ativo": usuario.is_active,
        "data_cadastro": usuario.date_joined,
        "ultimo_acesso": usuario.last_login,
        "senha_temporaria_pendente": (
            not (usuario.is_staff or usuario.is_superuser)
            and usuario.last_login is None
        ),
    }

    return JsonResponse(dados)


@transaction.atomic
def salvar_usuario(request):
    if request.method != "POST":
        return JsonResponse(
            {"sucesso": False, "mensagem": "Método não permitido."},
            status=405,
        )

    usuario_id = (request.POST.get("usuario_id") or "").strip()
    username = (request.POST.get("username") or "").strip()
    nome = (request.POST.get("nome") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()
    is_staff = request.POST.get("is_staff") == "on"
    ativo = request.POST.get("ativo") == "on"
    senha = request.POST.get("senha") or ""
    confirmar_senha = request.POST.get("confirmar_senha") or ""

    if usuario_id and int(usuario_id) == request.user.id:
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Não é permitido editar ou definir senha temporária para a própria conta por esta tela. Utilize 'Meu perfil'.",
            },
            status=400,
        )

    if not username or not nome or not email:
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Preencha nome, usuário e e-mail.",
            },
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Informe um e-mail válido."},
            status=400,
        )

    qs_username = User.objects.filter(username__iexact=username)
    qs_email = User.objects.filter(email__iexact=email)
    if usuario_id:
        qs_username = qs_username.exclude(id=usuario_id)
        qs_email = qs_email.exclude(id=usuario_id)

    if qs_username.exists():
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Já existe um usuário com este nome de login.",
            },
            status=400,
        )

    if qs_email.exists():
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Já existe um usuário cadastrado com este e-mail.",
            },
            status=400,
        )

    if usuario_id:
        try:
            usuario = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"sucesso": False, "mensagem": "Usuário não encontrado."},
                status=404,
            )

        mensagem = "Usuário atualizado com sucesso."
    else:
        if not senha:
            return JsonResponse(
                {
                    "sucesso": False,
                    "mensagem": "Gere uma senha temporária para o novo usuário.",
                },
                status=400,
            )
        usuario = User(last_login=None)
        mensagem = "Usuário cadastrado com sucesso."

    usuario.username = username
    usuario.first_name = nome
    usuario.email = email
    usuario.is_staff = is_staff
    usuario.is_active = ativo

    if senha or confirmar_senha:
        if confirmar_senha and senha != confirmar_senha:
            return JsonResponse(
                {"sucesso": False, "mensagem": "As senhas informadas não coincidem."},
                status=400,
            )
        try:
            validate_password(senha, user=usuario)
        except ValidationError as erro:
            return JsonResponse(
                {"sucesso": False, "mensagem": " ".join(erro.messages)},
                status=400,
            )
        usuario.set_password(senha)
        usuario.last_login = None

    usuario.save()

    return JsonResponse(
        {
            "sucesso": True,
            "usuario_id": usuario.id,
            "mensagem": mensagem,
        },
        status=200,
    )


@transaction.atomic
def excluir_usuario(request):
    if request.method != "DELETE":
        return JsonResponse(
            {"sucesso": False, "mensagem": "Método não permitido."},
            status=405,
        )

    try:
        dados = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Dados inválidos."},
            status=400,
        )

    usuario_id = dados.get("usuario_id")
    if not usuario_id:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Usuário não informado."},
            status=400,
        )

    if int(usuario_id) == request.user.id:
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Você não pode excluir a sua própria conta.",
            },
            status=400,
        )

    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Usuário não encontrado."},
            status=404,
        )

    usuario.delete()

    return JsonResponse(
        {
            "sucesso": True,
            "usuario_id": int(usuario_id),
            "mensagem": "Usuário excluído com sucesso.",
        },
        status=200,
    )


def detalhar_perfil(request):
    if request.method != "GET":
        return JsonResponse(
            {"sucesso": False, "mensagem": "Método não permitido."},
            status=405,
        )

    usuario = request.user
    return JsonResponse(
        {
            "username": usuario.username,
            "nome": usuario.first_name,
            "email": usuario.email,
            "perfil": (
                "Administrador"
                if (usuario.is_staff or usuario.is_superuser)
                else "Colaborador"
            ),
        }
    )


@transaction.atomic
def salvar_perfil(request):
    if request.method != "POST":
        return JsonResponse(
            {"sucesso": False, "mensagem": "Método não permitido."},
            status=405,
        )

    usuario = request.user
    nome = (request.POST.get("nome") or "").strip()
    username = (request.POST.get("username") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()

    senha_atual = request.POST.get("senha_atual") or ""
    nova_senha = request.POST.get("nova_senha") or ""
    confirmar_nova_senha = request.POST.get("confirmar_nova_senha") or ""

    if not nome or not username or not email:
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Preencha nome, usuário e e-mail.",
            },
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"sucesso": False, "mensagem": "Informe um e-mail válido."},
            status=400,
        )

    if User.objects.filter(username__iexact=username).exclude(id=usuario.id).exists():
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Este nome de usuário já está em uso.",
            },
            status=400,
        )

    if User.objects.filter(email__iexact=email).exclude(id=usuario.id).exists():
        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": "Este e-mail já está em uso por outra conta.",
            },
            status=400,
        )

    # Atualiza exclusivamente os campos básicos permitidos ao próprio usuário,
    # bloqueando qualquer tentativa de escalonamento de privilégio.
    usuario.first_name = nome
    usuario.username = username
    usuario.email = email
    campos_atualizados = ["first_name", "username", "email"]

    if senha_atual or nova_senha or confirmar_nova_senha:
        if not (senha_atual and nova_senha and confirmar_nova_senha):
            return JsonResponse(
                {
                    "sucesso": False,
                    "mensagem": "Para alterar a senha, preencha a senha atual, a nova senha e a confirmação.",
                },
                status=400,
            )

        if not usuario.check_password(senha_atual):
            return JsonResponse(
                {
                    "sucesso": False,
                    "mensagem": "A senha atual informada está incorreta.",
                },
                status=400,
            )

        if nova_senha != confirmar_nova_senha:
            return JsonResponse(
                {
                    "sucesso": False,
                    "mensagem": "A nova senha e a confirmação não coincidem.",
                },
                status=400,
            )

        try:
            validate_password(nova_senha, user=usuario)
        except ValidationError as erro:
            return JsonResponse(
                {"sucesso": False, "mensagem": " ".join(erro.messages)},
                status=400,
            )

        usuario.set_password(nova_senha)
        campos_atualizados.append("password")

    usuario.save(update_fields=campos_atualizados)

    if "password" in campos_atualizados:
        update_session_auth_hash(request, usuario)

    primeiro_nome = nome.split()[0] if nome.split() else usuario.username

    return JsonResponse(
        {
            "sucesso": True,
            "mensagem": "Perfil atualizado com sucesso.",
            "saudacao": primeiro_nome,
        },
        status=200,
    )
