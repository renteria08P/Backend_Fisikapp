from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Laboratorio, Categoria, Objetivo, PalabraClave

admin.site.register(Laboratorio)
admin.site.register(Categoria)
admin.site.register(Objetivo)
admin.site.register(PalabraClave)