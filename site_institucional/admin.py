from django.contrib import admin

from site_institucional.models import Doador


@admin.register(Doador)
class DoadorAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor", "criado_em", "aprovado")
    list_filter = ("aprovado",)
    list_editable = ("aprovado",)
    ordering = ("-criado_em",)
    search_fields = ("nome",)
    actions = ["aprovar_doacoes"]

    @admin.action(description="Aprovar doações selecionadas (Pix conferido)")
    def aprovar_doacoes(self, request, queryset):
        total = queryset.update(aprovado=True)
        self.message_user(request, f"{total} doação(ões) aprovada(s).")
