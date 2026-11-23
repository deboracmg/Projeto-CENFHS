from django import forms

from painel_administrativo.models.servicos import Servico, Turma


class FiltroPeriodoForm(forms.Form):
    data_inicio = forms.DateField(
        label="Data inicial", required=False, input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    data_fim = forms.DateField(
        label="Data final", required=False, input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

    def clean(self):
        dados = super().clean()
        inicio = dados.get("data_inicio")
        fim = dados.get("data_fim")
        if inicio and fim and inicio > fim:
            self.add_error("data_fim", "A data final deve ser igual ou posterior à data inicial.")
        return dados


class FiltroTurmasForm(FiltroPeriodoForm):
    curso = forms.ModelChoiceField(
        label="Curso", required=False, empty_label="Todos",
        queryset=Servico.objects.filter(turmas__isnull=False).distinct().order_by("nome", "pk"),
    )
    turma = forms.ModelChoiceField(
        label="Turma", required=False, empty_label="Todas",
        queryset=Turma.objects.select_related("servico").order_by("servico__nome", "descricao", "pk"),
    )

    def clean(self):
        dados = super().clean()
        curso = dados.get("curso")
        turma = dados.get("turma")
        if curso and turma and turma.servico_id != curso.pk:
            self.add_error("turma", "Escolha uma turma do curso selecionada.")
        return dados


class FiltroEncontrosForm(FiltroPeriodoForm):
    servico = forms.ModelChoiceField(
        label="Atividade ou evento", required=False, empty_label="Todos",
        queryset=Servico.objects.filter(
            tipo__in=[Servico.Tipo.ATIVIDADE, Servico.Tipo.EVENTO]
        ).order_by("nome", "pk"),
    )
