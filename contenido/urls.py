from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

from .views import (
    conceptos_list,
    conceptos_detalle,
    practicas_list,
    practicas_detalle,
    procedimientos_list,
    procedimientos_detalle,
    lista_formulas,
    detalle_formula,
    recursos_list,
    recursos_detalle,

)

# ==========================================
# ROUTER
# ==========================================

# ==========================================
# URLS
# ==========================================

router = DefaultRouter()


urlpatterns = [

    # Conceptos
    path('conceptos/', conceptos_list),
    path('conceptos/<int:pk>/', conceptos_detalle),

    # Recursos
    path('recursos/', recursos_list),
    path('recursos/<int:pk>/', recursos_detalle),

    # Practicas
    path('practicas/', practicas_list),
    path('practicas/<int:pk>/', practicas_detalle),

    # Procedimientos
    path('procedimientos/', procedimientos_list),
    path('procedimientos/<int:pk>/', procedimientos_detalle),

    # Formulas
    path('formulas/', lista_formulas),
    path('formulas/<int:pk>/', detalle_formula),

]

# ==========================================
# RUTAS AUTOMÁTICAS
# ==========================================
urlpatterns += router.urls