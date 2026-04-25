from django.urls import path
from laboratorios.api.views import generar_contenido_ia

urlpatterns = [
    path('generar-contenido/', generar_contenido_ia),
]