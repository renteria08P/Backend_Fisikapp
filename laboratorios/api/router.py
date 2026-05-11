from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import generar_contenido_ia
from .views import (
    LaboratorioViewSet,
    CategoriaViewSet,
    PalabraClaveViewSet,
    ObjetivoViewSet,
    LaboratorioProfesorViewSet
)


router_laboratorios = DefaultRouter()
router_laboratorios.register(r'laboratorios', LaboratorioViewSet, basename='laboratorios')

router_categorias = DefaultRouter()
router_categorias.register(r'categorias', CategoriaViewSet, basename='categorias')

router_palabras = DefaultRouter()
router_palabras.register(r'palabras-clave', PalabraClaveViewSet, basename='palabras-clave')

router_objetivos = DefaultRouter()
router_objetivos.register(r'objetivos', ObjetivoViewSet, basename='objetivos')

router = DefaultRouter()
router.register(r'laboratorio-profesor',LaboratorioProfesorViewSet,  basename='laboratorio-profesor')

urlpatterns = [
    path('api/laboratorios/generar-ia/', generar_contenido_ia, name='generar_ia'),
]



