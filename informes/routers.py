from rest_framework.routers import DefaultRouter
from .views import InformeViewSet
from .views import ResultadoViewSet

router = DefaultRouter()
router.register(r'informes', InformeViewSet, basename = 'informes')
router.register(r'resultados', ResultadoViewSet, basename = 'resultados')

urlpatterns = router.urls