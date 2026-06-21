from django.contrib import admin

from .models import (
    ConceptosBasicos,
    Recursos,
    Practica,
    Procedimiento,
    Formula,
    PracticaEstudiante
)

admin.site.register(ConceptosBasicos)
admin.site.register(Recursos)

admin.site.register(Practica)

admin.site.register(Procedimiento)

admin.site.register(Formula)

admin.site.register(PracticaEstudiante)