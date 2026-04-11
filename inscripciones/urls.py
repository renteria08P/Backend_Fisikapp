from django.urls import path
from .views import (inscribir_usuario, listar_inscripciones, 
                    detalle_inscripcion
)

urlpatterns = [
    path('inscribir/', inscribir_usuario),
    path('inscripciones/', listar_inscripciones),
    path('inscripciones/<int:pk>/', detalle_inscripcion),
   
]