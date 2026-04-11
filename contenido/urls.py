from django.urls import path
from . import views 

from .views import ( conceptos_list, conceptos_detalle,
                    practicas_list, practicas_detalle,
                    procedimientos_list, procedimientos_detalle,
                    lista_formulas, lista_bibliografia,
                    detalle_formula, detalle_bibliografia
)

urlpatterns = [

     # Conceptos
    path('conceptos/', conceptos_list),
    path('conceptos/<int:pk>/', conceptos_detalle),

    # Practicas
    path('practicas/', practicas_list),
    path('practicas/<int:pk>/', practicas_detalle),

    # Procedimientos
    path('procedimientos/', procedimientos_list),
    path('procedimientos/<int:pk>/', procedimientos_detalle),

    #Formulas y Bibliografia
    path('formulas/', lista_formulas),
    path('formulas/<int:pk>/', detalle_formula),

    path('bibliografia/', lista_bibliografia),
    path('bibliografia/<int:pk>/', detalle_bibliografia),
    
]