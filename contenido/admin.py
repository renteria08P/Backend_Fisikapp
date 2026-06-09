from django.contrib import admin

from .models import (
    ConceptosBasicos,
    Recursos,

    PlantillaPractica,
    Practica,

    PlantillaProcedimiento,
    Procedimiento,

    PlantillaFormula,
    Formula,

    PlantillaBibliografia,
    Bibliografia,

    PracticaEstudiante
)

admin.site.register(ConceptosBasicos)
admin.site.register(Recursos)

admin.site.register(PlantillaPractica)
admin.site.register(Practica)

admin.site.register(PlantillaProcedimiento)
admin.site.register(Procedimiento)

admin.site.register(PlantillaFormula)
admin.site.register(Formula)

admin.site.register(PlantillaBibliografia)
admin.site.register(Bibliografia)

admin.site.register(PracticaEstudiante)