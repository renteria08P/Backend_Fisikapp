from django.contrib import admin
from .models import (
    Laboratorio,
    Categoria,
    ObjetivoGeneral,
    ObjetivoEspecifico,
    PalabraClave
)

admin.site.register(Laboratorio)
admin.site.register(Categoria)
admin.site.register(ObjetivoGeneral)
admin.site.register(ObjetivoEspecifico)
admin.site.register(PalabraClave)