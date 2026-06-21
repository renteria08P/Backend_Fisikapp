from django.contrib import admin
from .models import (
    Laboratorio,
    Categoria,
    ObjetivoGeneral,
    ObjetivoEspecifico,
)

admin.site.register(Laboratorio)
admin.site.register(Categoria)
admin.site.register(ObjetivoGeneral)
admin.site.register(ObjetivoEspecifico)