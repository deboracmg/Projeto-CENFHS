from django.shortcuts import render
from django.http import JsonResponse


from painel_administrativo.models.servicos import Aula, Avaliacao, Matricula, Servico, Turma

def buscar_servicos(request):
    if request.method != "GET":
        return JsonResponse({
            "sucesso": False,            
            "mensagem": "Método não permitido."
            },
            status=405
        )

    termo = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    if termo:
        servicos = Servico.objects.filter(
            ativo=True,
            tipo=tipo,
            nome__icontains=termo,
        )[:10]
    else : 
        servicos = Servico.objects.filter(
            ativo=True,
            tipo=tipo,
        ).order_by("-data_cadastro")[:10]
    

    resultados = [
        {
            "id": servico.id,
            "nome": servico.nome,
            "tipo": servico.get_tipo_display(),
        }
        for servico in servicos
    ]

    return JsonResponse({"resultados": resultados})


# Centro de Formação
def cursos(request):
    cursos = Servico.objects.filter(tipo=Servico.Tipo.CURSO)

    return render(
        request,
        "painel/servicos/cursos.html",
        {"cursos": cursos}
    )


def turmas(request):
    turmas = Turma.objects.select_related("responsavel").all().order_by("-data_cadastro")

    return render(
        request,
        "painel/servicos/turmas.html",
        {"turmas": turmas}
    )


def matriculas(request):
    matriculas = Matricula.objects.select_related("aluno", "turma__servico").all()

    return render(
        request,
        "painel/servicos/matriculas.html",
        {"matriculas": matriculas}
    )


def aulas(request):
    aulas = Aula.objects.select_related("turma").all()

    return render(
        request,
        "painel/servicos/aulas.html",
        {"aulas": aulas}
    )


def atividades(request):
    atividades = Servico.objects.filter(tipo=Servico.Tipo.ATIVIDADE)

    return render(
        request,
        "painel/servicos/atividades.html",
        {"atividades": atividades}
    )


def eventos(request):
    eventos = Servico.objects.filter(tipo=Servico.Tipo.EVENTO)

    return render(
        request,
        "painel/servicos/eventos.html",
        {"eventos": eventos}
    )


# Casa de Apoio
def avaliacoes(request):
    avaliacoes = Avaliacao.objects.select_related("tratamento__paciente").all()

    return render(
        request,
        "painel/servicos/avaliacoes.html",
        {"avaliacoes": avaliacoes}
    )


