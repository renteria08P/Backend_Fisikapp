from rest_framework.routers import DefaultRouter
from .views import (
    LaboratorioViewSet,
    CategoriaViewSet,
    PalabraClaveViewSet,
    ObjetivoViewSet
)

router = DefaultRouter()

router.register(r'laboratorios', LaboratorioViewSet, basename='laboratorios')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'palabras-clave', PalabraClaveViewSet, basename='palabras-clave')
router.register(r'objetivos', ObjetivoViewSet, basename='objetivos')

urlpatterns = router.urls