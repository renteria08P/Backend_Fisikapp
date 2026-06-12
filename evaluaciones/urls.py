from django.urls import path, include
from rest_framework.routers import DefaultRouter

from evaluaciones.views import (
    EvaluacionProfesorViewSet,
    EvaluacionIAViewSet
)

router = DefaultRouter()

router.register(
    r'evaluaciones-ia',
    EvaluacionIAViewSet,
    basename='evaluaciones-ia'
)

router.register(
    r'evaluacion-profesor',
     EvaluacionProfesorViewSet,
    basename='evaluacion-profesor'
)

urlpatterns = router.urls