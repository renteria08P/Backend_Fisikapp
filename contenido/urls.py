from django.urls import path, include
from . import views 
from rest_framework.routers import DefaultRouter 

from .views import (
    ConceptosBasicosViewSet,
    PracticasViewSet,
    ProcedimientosViewSet,
    FormulasViewSet,
    BibliografiaViewSet,
    RecursosViewSet,
    conceptos_list, conceptos_detalle,
    practicas_list, practicas_detalle,
    procedimientos_list, procedimientos_detalle,
    lista_formulas, detalle_formula,
    lista_bibliografia, detalle_bibliografia,
    recursos_list, recursos_detalle
)

router = DefaultRouter()
router.register(r'conceptos', ConceptosBasicosViewSet)
router.register(r'practicas', PracticasViewSet)
router.register(r'procedimientos', ProcedimientosViewSet)
router.register(r'formulas', FormulasViewSet)
router.register(r'bibliografia', BibliografiaViewSet)
router.register(r'recursos', RecursosViewSet)

urlpatterns = [
 
     # Conceptos
    path('conceptos/', conceptos_list),
    path('conceptos/<int:pk>/', conceptos_detalle),

    # Recursos
    path('recursos/', views.recursos_list),
    path('recursos/<int:pk>/', views.recursos_detalle),

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