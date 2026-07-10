from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    DashboardAdminViewSet,
    LaboratorioProfesorViewSet,
    PlantillaLaboratorioViewSet,
    GrupoAcademicoViewSet,
    AsignacionViewSet,
    InscripcionViewSet,
    LaboratorioEstudianteViewSet,
    PlantillaObjetivoEspecificoViewSet,
    PlantillaObjetivoGeneralViewSet,
    LaboratorioProfesorAdminViewSet,  
    PreguntaLaboratorioViewSet,
    SimulacionARViewSet,  
)


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
    r'laboratorio-profesor',
    LaboratorioProfesorViewSet,
    basename='laboratorio-profesor'
)

router.register(
    r'laboratorio-admin',
    LaboratorioProfesorAdminViewSet,
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

router.register(
    r'dashboard-admin',
    DashboardAdminViewSet,
    basename='dashboard-admin'
)

router.register(
    r'simulaciones-ar',
    SimulacionARViewSet,
    basename='simulaciones-ar'
)

router.register(
    r'preguntas-laboratorio',
    PreguntaLaboratorioViewSet,
    basename='preguntas-laboratorio'
)

urlpatterns = [
    
]

urlpatterns += router.urls