from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  filters
from rest_framework.decorators import action
from inscripciones.models import Inscripcion
from django_filters.rest_framework import DjangoFilterBackend

from laboratorios.models import GrupoAcademico
from .serializers import GrupoAcademicoSerializer, LaboratorioEstudianteListSerializer
from laboratorios.models import PlantillaLaboratorio
from .serializers import PlantillaLaboratorioSerializer

from users.permissions import IsAdminOrSuperAdmin, IsProfesor

from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
    
)

from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave
)

from .serializers import (
    LaboratorioProfesorAdminSerializer,
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    LaboratorioProfesorSerializer,
    LaboratorioEstudianteSerializer,
)


class PlantillaLaboratorioViewSet(ModelViewSet):
    queryset = PlantillaLaboratorio.objects.all()
    serializer_class = PlantillaLaboratorioSerializer
    permission_classes = [IsAuthenticated]

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class PalabraClaveViewSet(ModelViewSet):
    queryset = PalabraClave.objects.all()
    serializer_class = PalabraClaveSerializer
    permission_classes = [IsAuthenticated]

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

from laboratorios.models import Asignacion
from .serializers import AsignacionSerializer

class AsignacionViewSet(ModelViewSet):

    serializer_class = AsignacionSerializer
    permission_classes = [IsAuthenticated, IsProfesor]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Asignacion.objects.none()

        return Asignacion.objects.filter(
            profesor=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            profesor=self.request.user
        )

from inscripciones.models import Inscripcion
from inscripciones.serializers import InscripcionSerializer

class InscripcionViewSet(ModelViewSet):

    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.rol == "estudiante":
            return Inscripcion.objects.filter(
                estudiante=self.request.user
            )

        return Inscripcion.objects.all()

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

    # =====================================================
    # MIS LABORATORIOS
    # =====================================================
    @action(detail=False, methods=['get'])
    def mis_laboratorios(self, request):

        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )

        return Response(serializer.data)

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
# LABORATORIOS - ADMIN
# =========================================================
class LaboratorioAdminViewSet(ModelViewSet):
    serializer_class = LaboratorioProfesorAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get_queryset(self):
        return Laboratorio.objects.all().order_by(
        '-fecha_actualizacion'
    )

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

        return Laboratorio.objects.filter(
            asignaciones__inscripciones__estudiante=
            self.request.user
        ).distinct()

    def retrieve(self, request, *args, **kwargs):

        laboratorio = self.get_object()

        inscrito = Inscripcion.objects.filter(
            estudiante=request.user,
            asignacion__laboratorio=laboratorio
        ).exists()

        if not inscrito:

            return Response(
                {
                    "error":
                    "No estás inscrito en este laboratorio"
                },
                status=403
            )

        serializer = self.get_serializer(
            laboratorio
        )

        return Response(serializer.data)