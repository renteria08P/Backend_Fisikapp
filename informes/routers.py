from rest_framework.routers import DefaultRouter
from .views import (
    InformeViewSet,
    ResultadoViewSet,
    ConclusionesViewSet,
    RecomendacionesViewSet
)

router = DefaultRouter()
router.register(r'informes', InformeViewSet, basename='informes')
router.register(r'resultados', ResultadoViewSet, basename='resultados')
router.register(r'conclusiones', ConclusionesViewSet, basename='conclusiones')
router.register(r'recomendaciones', RecomendacionesViewSet, basename='recomendaciones')