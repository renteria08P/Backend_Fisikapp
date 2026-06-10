from rest_framework.routers import DefaultRouter

from .views import  (
    EntregaViewSet, 
    PreguntaViewSet, 
    RespuestaViewSet, 
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
    r'preguntas',
    PreguntaViewSet,
    basename='preguntas'
)

router.register(
    r'respuestas',
    RespuestaViewSet,
    basename='respuestas'
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