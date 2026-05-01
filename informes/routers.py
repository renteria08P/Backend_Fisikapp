from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InformeViewSet,
    ResultadoViewSet,
    ConclusionesViewSet,
    RecomendacionesViewSet
)

router = DefaultRouter()
router.register(r'informes', InformeViewSet)
router.register(r'resultados', ResultadoViewSet)
router.register(r'conclusiones', ConclusionesViewSet)
router.register(r'recomendaciones', RecomendacionesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
