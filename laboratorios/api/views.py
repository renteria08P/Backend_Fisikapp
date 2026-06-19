import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response
from rest_framework import status, filters
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action

from django_filters.rest_framework import (
    DjangoFilterBackend
)

from users.permissions import (
    IsAdminOrSuperAdmin,
    IsProfesor
)

from laboratorios.models import (
    Laboratorio,
    Categoria,
    GrupoAcademico,
    Asignacion,
    PlantillaLaboratorio,
    PlantillaObjetivoGeneral,
    PlantillaObjetivoEspecifico
)

from inscripciones.models import (
    Inscripcion
)

from inscripciones.serializers import (
    InscripcionSerializer
)

from .serializers import (
    CategoriaSerializer,
    PlantillaLaboratorioSerializer,
    GrupoAcademicoSerializer,
    AsignacionSerializer,
    LaboratorioSerializer,
    LaboratorioProfesorSerializer,
    LaboratorioProfesorAdminSerializer,
    LaboratorioEstudianteSerializer,
    LaboratorioEstudianteListSerializer,
    PlantillaObjetivoGeneralSerializer,
    PlantillaObjetivoEspecificoSerializer
)

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class PlantillaLaboratorioViewSet(ModelViewSet):

    queryset = PlantillaLaboratorio.objects.all()

    serializer_class = (
        PlantillaLaboratorioSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @swagger_auto_schema(
        operation_summary="Crear plantilla de laboratorio",
        operation_description="""
        Permite registrar una nueva plantilla de laboratorio
        que servirá como base para la creación de laboratorios.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Listar plantillas de laboratorio",
        operation_description="""
        Retorna todas las plantillas de laboratorio registradas
        en el sistema. Las plantillas sirven como base para que
        los profesores creen nuevos laboratorios.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Detalle de plantilla",
        operation_description="""
        Retorna toda la información de una plantilla de laboratorio.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class GrupoAcademicoViewSet(ModelViewSet):

    serializer_class = GrupoAcademicoSerializer
    permission_classes = [IsAuthenticated, IsProfesor]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return GrupoAcademico.objects.none()

        return GrupoAcademico.objects.filter(
            profesor=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            profesor=self.request.user
        )

    @swagger_auto_schema(
        operation_summary="Listar grupos académicos",
        operation_description="""
        Retorna los grupos académicos asociados al profesor
        autenticado.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear grupo académico",
        operation_description="""
        Permite al profesor registrar un nuevo grupo académico.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Detalle de grupo académico",
        operation_description="""
        Obtiene la información completa de un grupo académico.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class AsignacionViewSet(ModelViewSet):

    serializer_class = AsignacionSerializer
    permission_classes = [IsAuthenticated, IsProfesor]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Asignacion.objects.none()
        
        return Asignacion.objects.filter(
            laboratorio__profesor=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Listar asignaciones",
        operation_description="""
        Obtiene las asignaciones de laboratorios realizadas
        por el profesor autenticado.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear asignación",
        operation_description="""
        Asigna un laboratorio a un grupo académico
        durante un rango de fechas determinado.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Detalle de asignación",
        operation_description="""
        Consulta la información completa de una asignación.
        """
    )

    @action(
        detail=True,
        methods=['get']
    )
    def qr(self, request, pk=None):

        asignacion = self.get_object()

        codigo = asignacion.codigo_ingreso

        qr = qrcode.make(codigo)

        buffer = BytesIO()

        qr.save(
            buffer,
            format='PNG'
        )

        buffer.seek(0)

        return HttpResponse(
            buffer.getvalue(),
            content_type='image/png'
        )
    
    @action(
        detail=True,
        methods=['get'],
        url_path='qr-info'
    )
    def qr_info(self, request, pk=None):

        asignacion = self.get_object()

        return Response({
            "id": asignacion.id,
            "laboratorio": asignacion.laboratorio.plantilla.titulo,
            "grupo": asignacion.grupo.nombre,
            "codigo": asignacion.codigo_ingreso,
            "qr_url": f"/api/asignaciones/{asignacion.id}/qr/"
        })

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class InscripcionViewSet(ModelViewSet):

    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if getattr(self.request.user, "rol", None) == "estudiante":
            return Inscripcion.objects.filter(
                estudiante=self.request.user
            )

        return Inscripcion.objects.all()

    @swagger_auto_schema(
        operation_summary="Listar inscripciones",
        operation_description="""
        Permite consultar las inscripciones de estudiantes
        a laboratorios asignados.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear inscripción",
        operation_description="""
        Permite inscribir un estudiante a un laboratorio
        mediante una asignación existente.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class LaboratorioViewSet(ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [IsAuthenticated]

    # Filtros, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'profesor',
        'estado',
        'generado_ia' 
        ]
    
    search_fields = [
        'codigo_lab',
        'resumen',
        'introduccion',
        'marco_teorico'
        ]

    ordering_fields = [
        'fecha_creacion',
        'fecha_actualizacion'
        ]
    
    ordering = ['fecha_creacion']  # orden por defecto

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {
                "mensaje": "Laboratorio creado con éxito",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


    def get_queryset(self):          
        queryset = Laboratorio.objects.all()
        nombre = self.request.query_params.get('nombre', None)  
        if nombre:
            queryset = queryset.filter(
        plantilla__titulo__icontains=nombre
    )
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(
            profesor=self.request.user
        )

    def get_permissions(self):
        if self.action == "cargar_estudiantes_excel":
            return [IsAuthenticated(), IsProfesor()]

        return [IsAuthenticated()]


# =========================================================
# Gestión de Laboratorios - Admin
# =========================================================
class LaboratorioProfesorAdminViewSet(
    ReadOnlyModelViewSet
):

    queryset = (
        Laboratorio.objects.all()
        .select_related(
            'plantilla',
            'plantilla__categoria',
            'profesor'
        )
    )

    serializer_class = (
        LaboratorioProfesorAdminSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrSuperAdmin
    ]

    @swagger_auto_schema(
        operation_summary="Auditoría de laboratorios",
        operation_description="""
        Permite a administradores y superadministradores
        consultar todos los laboratorios registrados.

        Información disponible:
        - Título del laboratorio
        - Categoría
        - Profesor creador
        - Estado
        - Fecha de última actualización
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Detalle de laboratorio",
        operation_description="""
        Retorna la información detallada de un laboratorio
        específico para fines de auditoría y seguimiento.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
# =========================================================
# LABORATORIO PROFESOR
# =========================================================
class LaboratorioProfesorViewSet(ModelViewSet):

    serializer_class = LaboratorioProfesorSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = [
        'estado',
        'generado_ia'
    ]

    search_fields = [
        'codigo_lab'
    ]

    ordering_fields = [
        'fecha_creacion',
        'fecha_actualizacion'
    ]

    ordering = ['-fecha_creacion']

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Laboratorio.objects.none()

        return Laboratorio.objects.filter(
            profesor=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            profesor=self.request.user
        ) 

    @swagger_auto_schema(
        operation_summary="Crear laboratorio",
        operation_description="""
        Permite al profesor crear un laboratorio
        basado en una plantilla existente.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Listar laboratorios",
        operation_description="""
        Retorna todos los laboratorios creados
        por el profesor autenticado.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Detalle de laboratorio",
        operation_description="""
        Obtiene la información completa de un laboratorio
        creado por el profesor.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    # =====================================================
    # ESTUDIANTES DEL LABORATORIO
    # =====================================================
    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):

        laboratorio = self.get_object()

        inscripciones = Inscripcion.objects.filter(
            asignacion__laboratorio=laboratorio
        ).select_related(
            'estudiante'
        )

        data = []

        for inscripcion in inscripciones:

            data.append({
                "id": inscripcion.estudiante.id,
                "nombre": inscripcion.estudiante.nombre,
                "correo": inscripcion.estudiante.correo,
                "fecha_inscripcion": inscripcion.fecha_inscripcion
            })

        return Response(data)
    

    @swagger_auto_schema(
        operation_summary="Mis laboratorios",
        operation_description="""
        Retorna los laboratorios creados por el profesor
        autenticado.
        """
    )
    @action(detail=False, methods=['get'])
    def mis_laboratorios(self, request):

        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)
    
    @swagger_auto_schema(
    operation_summary="Estudiantes inscritos",
    operation_description="""
    Obtiene el listado de estudiantes inscritos
    en un laboratorio específico.
    """
)
    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):

        laboratorio = self.get_object()

        inscripciones = Inscripcion.objects.filter(
            asignacion__laboratorio=laboratorio
        ).select_related(
            'estudiante'
        )

        data = []

        for inscripcion in inscripciones:
            data.append({
                "id": inscripcion.estudiante.id,
                "nombre": inscripcion.estudiante.nombre,
                "correo": inscripcion.estudiante.correo,
                "fecha_inscripcion": inscripcion.fecha_inscripcion
            })

        return Response(data)

    # =====================================================
    # PROGRESO ESTUDIANTE (PENDIENTE)
    # =====================================================

    # @action(detail=True, methods=['get'])
    # def progreso(self, request, pk=None):
    #     laboratorio = self.get_object()
    #     etapas = Etapa.objects.filter(
    #         laboratorio=laboratorio
    #     ).order_by('orden')
    #
    #     total = etapas.count()
    #     completadas = 0
    #     resultado = []
    #
    #     for etapa in etapas:
    #
    #         prog = ProgresoEstudiante.objects.filter(
    #             estudiante=request.user,
    #             etapa=etapa
    #         ).first()
    #
    #         hecho = prog.completada if prog else False
    #
    #         if hecho:
    #             completadas += 1
    #
    #         resultado.append({
    #             "etapa_id": etapa.id,
    #             "nombre": etapa.nombre,
    #             "completada": hecho
    #         })
    #
    #     return Response({
    #         "porcentaje": (
    #             int((completadas / total) * 100)
    #             if total > 0 else 0
    #         ),
    #         "etapas": resultado
    #     })

    # =====================================================
    # COMPLETAR ETAPA (PENDIENTE)
    # =====================================================

    # @action(
    #     detail=True,
    #     methods=['post'],
    #     url_path='etapas/(?P<etapa_id>[^/.]+)/completar'
    # )
    # def completar_etapa(
    #     self,
    #     request,
    #     pk=None,
    #     etapa_id=None
    # ):
    #
    #     laboratorio = self.get_object()
    #
    #     try:
    #         etapa = Etapa.objects.get(
    #             id=etapa_id,
    #             laboratorio=laboratorio
    #         )
    #
    #     except Etapa.DoesNotExist:
    #         return Response(
    #             {"error": "Etapa no encontrada"},
    #             status=404
    #         )
    #
    #     prog, _ = (
    #         ProgresoEstudiante.objects.get_or_create(
    #             estudiante=request.user,
    #             etapa=etapa
    #         )
    #     )
    #
    #     prog.completada = True
    #     prog.fecha_completado = date.today()
    #     prog.save()
    #
    #     return Response({
    #         "mensaje":
    #         f"Etapa '{etapa.nombre}' completada"
    #     })

    # =====================================================
    # CARGAR ESTUDIANTES EXCEL (PENDIENTE)
    # =====================================================

    # @action(
    #     detail=True,
    #     methods=['post'],
    #     url_path='cargar-estudiantes'
    # )
    # def cargar_estudiantes_excel(
    #     self,
    #     request,
    #     pk=None
    # ):
    #
    #     laboratorio = self.get_object()
    #
    #     archivo = request.FILES.get('file')
    #
    #     if not archivo:
    #         return Response(
    #             {"error": "No se envió archivo"},
    #             status=400
    #         )
    #
    #     try:
    #         df = pd.read_excel(archivo)
    #
    #     except Exception:
    #         return Response(
    #             {"error": "Archivo inválido"},
    #             status=400
    #         )
    #
    #     creados = 0
    #     errores = []
    #
    #     with transaction.atomic():
    #
    #         for index, row in df.iterrows():
    #
    #             try:
    #
    #                 usuario = Users.objects.get(
    #                     correo=row['correo']
    #                 )
    #
    #                 if usuario.rol != "estudiante":
    #
    #                     errores.append(
    #                         f"Fila {index}: "
    #                         f"el usuario no es estudiante"
    #                     )
    #
    #                     continue
    #
    #                 inscripcion, created = (
    #                     Inscripcion.objects.get_or_create(
    #                         usuario=usuario,
    #                         laboratorio=laboratorio,
    #                         defaults={
    #                             "fecha_inscripcion":
    #                             date.today()
    #                         }
    #                     )
    #                 )
    #
    #                 if created:
    #                     creados += 1
    #
    #                 else:
    #                     errores.append(
    #                         f"Fila {index}: ya inscrito"
    #                     )
    #
    #             except Users.DoesNotExist:
    #
    #                 errores.append(
    #                     f"Fila {index}: usuario no existe"
    #                 )
    #
    #     return Response({
    #         "mensaje": "Inscripción finalizada",
    #         "creados": creados,
    #         "errores": errores
    #     })

# =========================================================
# LABORATORIO ESTUDIANTE
# =========================================================
class LaboratorioEstudianteViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.action == "list":
            return LaboratorioEstudianteListSerializer

        return LaboratorioEstudianteSerializer

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Laboratorio.objects.none()

        return Laboratorio.objects.filter(
            asignaciones__inscripciones__estudiante=
            self.request.user
        ).distinct()
    

    @swagger_auto_schema(
        operation_summary="Laboratorios del estudiante",
        operation_description="""
        Retorna los laboratorios en los que el estudiante
        autenticado se encuentra inscrito.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="Detalle de laboratorio",
        operation_description="""
        Permite al estudiante consultar el contenido completo
        de un laboratorio en el que se encuentra inscrito.
        """
    )
    def retrieve(self, request, *args, **kwargs):

        laboratorio = self.get_object()

        inscrito = Inscripcion.objects.filter(
            estudiante=request.user,
            asignacion__laboratorio=laboratorio
        ).exists()

        if not inscrito:
            return Response(
                {
                    "error": "No estás inscrito en este laboratorio"
                },
                status=403
            )

        serializer = self.get_serializer(laboratorio)

        return Response(serializer.data)

# =========================================================
# OBJETIVO GENERAL PLANTILLA
# =========================================================

class PlantillaObjetivoGeneralViewSet(
    ModelViewSet
):

    queryset = (
        PlantillaObjetivoGeneral.objects.all()
    )

    serializer_class = (
        PlantillaObjetivoGeneralSerializer
    )

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Listar objetivos generales",
        operation_description="""
        Retorna todos los objetivos generales
        asociados a plantillas de laboratorio.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# =========================================================
# OBJETIVO ESPECIFICO PLANTILLA
# =========================================================

class PlantillaObjetivoEspecificoViewSet(
    ModelViewSet
):

    queryset = (
        PlantillaObjetivoEspecifico.objects.all()
    )

    serializer_class = (
        PlantillaObjetivoEspecificoSerializer
    )

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Listar objetivos específicos",
        operation_description="""
        Retorna todos los objetivos específicos
        asociados a objetivos generales de plantillas.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)