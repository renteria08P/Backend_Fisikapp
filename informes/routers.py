from rest_framework.routers import DefaultRouter
from .views import (
    InformeViewSet,
    ResultadoViewSet,
    ConclusionesViewSet,
    RecomendacionesViewSet
)

router = DefaultRouter()

router.register('informes', InformeViewSet, basename='informes')
router.register('resultados', ResultadoViewSet, basename='resultados')
router.register('conclusiones', ConclusionesViewSet, basename='conclusiones')
router.register('recomendaciones', RecomendacionesViewSet, basename='recomendaciones')