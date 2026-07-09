from django.urls import path
from .views import (
    listar_inscripciones,
    detalle_inscripcion,
    mis_grupos,
    mis_laboratorios,
    inscribir_usuario,
    unirse_grupo,
    mis_grupos_movil,
    grupo_laboratorios_movil
)

from .views import grupo_laboratorios
from .views import detalle_asignacion
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

    path(
        'inscripciones/mis-grupos/',
        mis_grupos,
        name='mis-grupos'
    ),

    path(
        "grupos/unirse/",
        unirse_grupo,
        name="unirse-grupo"
    ),

    path(
        'estudiante/grupos/<int:grupo_id>/laboratorios/',
        grupo_laboratorios,
        name='grupo-laboratorios-estudiante'
    ),

    path(
        'estudiante/asignaciones/<int:asignacion_id>/detalle/',
        detalle_asignacion,
        name='detalle-asignacion'
    ),

    path(
        "grupos/mis-grupos/",
        mis_grupos_movil,
        name="mis-grupos-movil"
    ),

    path(
        "grupos/<int:grupo_id>/laboratorios/",
        grupo_laboratorios_movil,
        name="grupo-laboratorios-movil"
    ),
]