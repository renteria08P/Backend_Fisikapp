
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    LaboratorioAdminViewSet,
    LaboratorioViewSet,
    CategoriaViewSet,
    PalabraClaveViewSet,
    LaboratorioProfesorViewSet,
     PlantillaLaboratorioViewSet,
    GrupoAcademicoViewSet,
    AsignacionViewSet,
    InscripcionViewSet,
    LaboratorioEstudianteViewSet,
    PlantillaObjetivoEspecificoViewSet,
    PlantillaObjetivoGeneralViewSet,

)

# =========================================================
# ROUTER PRINCIPAL
# =========================================================
router = DefaultRouter()

router.register(
    r'plantillas',
    PlantillaLaboratorioViewSet,
    basename='plantillas'
)

router.register(
    r'grupos',
    GrupoAcademicoViewSet,
    basename='grupos'
)

router.register(
    r'asignaciones',
    AsignacionViewSet,
    basename='asignaciones'
)

router.register(
    r'inscripciones',
    InscripcionViewSet,
    basename='inscripciones'
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
    r'laboratorio-profesor',
    LaboratorioProfesorViewSet,
    basename='laboratorio-profesor'
)

router.register(
    r'laboratorio-admin',
    LaboratorioAdminViewSet,
    basename='laboratorio-admin'
)


router.register(
    r'laboratorios-estudiante',
    LaboratorioEstudianteViewSet,
    basename='laboratorios-estudiante'
)

router.register(
    r'plantilla-objetivos-generales',
    PlantillaObjetivoGeneralViewSet,
    basename='plantilla-objetivos-generales'
)

router.register(
    r'plantilla-objetivos-especificos',
    PlantillaObjetivoEspecificoViewSet,
    basename='plantilla-objetivos-especificos'
)

# =========================================================
# URLS
# =========================================================
urlpatterns = [

   

]

# RUTAS AUTOMÁTICAS DEL ROUTER
urlpatterns += router.urls