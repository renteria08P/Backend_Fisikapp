from rest_framework.routers import DefaultRouter
from .views import InformeViewSet, ResultadoViewSet

router_informes = DefaultRouter()
router_informes.register(r'informes', InformeViewSet, basename='informes')

router_resultados = DefaultRouter()
router_resultados.register(r'resultados', ResultadoViewSet, basename='resultados')