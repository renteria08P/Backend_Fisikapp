from django.urls import path
from .views import (inscribir_usuario, listar_inscripciones, 
                    detalle_inscripcion, conceptos_list, conceptos_detalle,
                    practicas_list, practicas_detalle,
                    procedimientos_list, procedimientos_detalle 
)

urlpatterns = [
    path('inscribir/', inscribir_usuario),
    path('inscripciones/', listar_inscripciones),
    path('inscripciones/<int:pk>/', detalle_inscripcion),
    # Conceptos
    path('conceptos/', conceptos_list),
    path('conceptos/<int:pk>/', conceptos_detalle),

    # Practicas
    path('practicas/', practicas_list),
    path('practicas/<int:pk>/', practicas_detalle),

    # Procedimientos
    path('procedimientos/', procedimientos_list),
    path('procedimientos/<int:pk>/', procedimientos_detalle),
]