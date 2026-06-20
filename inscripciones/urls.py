from django.urls import path
from .views import (
    listar_inscripciones,
    detalle_inscripcion,
    mis_laboratorios,
    inscribir_usuario,
)
from .views import (
    GruposLaboratoriosView
)

urlpatterns = [
    path('inscripciones/', listar_inscripciones),
    path('inscripciones/<int:pk>/', detalle_inscripcion),
    path('inscripciones/mis-laboratorios/', mis_laboratorios),

    path(
        'inscripciones/inscribirse/',
        inscribir_usuario
    ),

    path(
        'grupos-laboratorios/',
        GruposLaboratoriosView.as_view()
),
]