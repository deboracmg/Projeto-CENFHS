from django.shortcuts import render
from painel_administrativo.models.pessoas import Paciente, Profissional


def listar_profissionais(request):
    profissionais = Profissional.objects.only(
        "id",
        "nome",
        "cpf",
        "data_nascimento",
        "telefone",
        "area_atuacao",
    )

    return render(
        request,
        "painel/pessoas/profissionais.html",
        {"profissionais": profissionais}
    )


# Casa de Apoio
def listar_pacientes(request):
    pacientes = Paciente.objects.only(
        "id",
        "nome",
        "cpf",
        "data_nascimento",
        "telefone",
    )

    return render(
        request,
        "painel/pessoas/pacientes.html",
        {"pacientes": pacientes}
    )
