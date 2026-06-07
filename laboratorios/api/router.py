
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    LaboratorioAdminViewSet,
    LaboratorioViewSet,
    CategoriaViewSet,
    PalabraClaveViewSet,
    LaboratorioProfesorViewSet,
    ObjetivoGeneralViewSet,
    ObjetivoEspecificoViewSet

)

# =========================================================
# ROUTER PRINCIPAL
# =========================================================
router = DefaultRouter()

router.register(
    r'laboratorios',
    LaboratorioViewSet,
    basename='laboratorios'
)

router.register(
    r'categorias',
    CategoriaViewSet,
    basename='categorias'
)

router.register(
    r'palabras-clave',
    PalabraClaveViewSet,
    basename='palabras-clave'
)

router.register(
    r'objetivos-generales',
    ObjetivoGeneralViewSet,
    basename='objetivos-generales'
)

router.register(
    r'objetivos-especificos',
    ObjetivoEspecificoViewSet,
    basename='objetivos-especificos'
)

router.register(
    r'laboratorio-profesor',
    LaboratorioProfesorViewSet,
    basename='laboratorio-profesor'
)


router.register(
    r'laboratorio-admin',
    LaboratorioAdminViewSet,
    basename='laboratorio-admin'
)

# =========================================================
# URLS
# =========================================================
urlpatterns = [

   

]

# RUTAS AUTOMÁTICAS DEL ROUTER
urlpatterns += router.urls