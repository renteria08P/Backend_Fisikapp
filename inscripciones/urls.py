from django.urls import path
from .views import (listar_inscripciones, 
                    detalle_inscripcion
)

urlpatterns = [
    path('inscripciones/', listar_inscripciones),
    path('inscripciones/<int:pk>/', detalle_inscripcion),
   
]