from rest_framework.routers import DefaultRouter

from .views import  (
    EntregaViewSet, 
    ResultadoPracticaViewSet, 
    ResultadoSimulacionViewSet
)


router = DefaultRouter()


router.register(
    r'entregas',
    EntregaViewSet,
    basename='entregas'
)

router.register(
    r'resultados-practica',
    ResultadoPracticaViewSet,
    basename='resultados-practica'
)

router.register(
    r'resultados-simulacion',
    ResultadoSimulacionViewSet,
    basename='resultados-simulacion'
)

urlpatterns = router.urls