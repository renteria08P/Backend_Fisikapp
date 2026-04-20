from rest_framework.routers import DefaultRouter
from .views import (
    InformeViewSet,
    ResultadoViewSet,
    ConclusionesViewSet,
    RecomendacionesViewSet
)

router = DefaultRouter()

router.register('informes', InformeViewSet)
router.register('resultados', ResultadoViewSet)
router.register('conclusiones', ConclusionesViewSet)
router.register('recomendaciones', RecomendacionesViewSet)
