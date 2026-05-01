from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InscripcionesViewSet,
    inscribir_usuario,
    listar_inscripciones,
    detalle_inscripcion
)

router = DefaultRouter()
router.register(r'inscripciones', InscripcionesViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Endpoints que ya tenías
    path('inscribir/', inscribir_usuario),
    path('inscripciones/', listar_inscripciones),
    path('inscripciones/<int:pk>/', detalle_inscripcion),
]
