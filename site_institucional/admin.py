from django.contrib import admin

from site_institucional.models import Doador


@admin.register(Doador)
class DoadorAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor", "criado_em")
    ordering = ("-criado_em",)
    search_fields = ("nome",)
