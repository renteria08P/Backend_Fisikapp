from django.contrib import admin

# Register your models here.

from .models import Inscripcion, ConceptosBasicos, Practicas, Procedimientos

admin.site.register(Inscripcion)
admin.site.register(ConceptosBasicos)
admin.site.register(Practicas)
admin.site.register(Procedimientos)