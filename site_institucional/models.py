from django.db import models


class Doador(models.Model):
    nome = models.CharField(max_length=120)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aprovado = models.BooleanField(
        "aprovado",
        default=False,
        help_text="Marque depois de conferir o Pix no extrato. "
        "Só doadores aprovados aparecem na lista pública do site.",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome

    @property
    def valor_formatado(self):
        if self.valor is None:
            return None
        return f"R$ {self.valor:.2f}".replace(".", ",")
