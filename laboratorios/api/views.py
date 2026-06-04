import random
import string

from laboratorios.models import Etapa, ProgresoEstudiante
from datetime import date
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  filters
from rest_framework.decorators import action
from django.db import transaction
from users.models import Users
import pandas as pd
from inscripciones.models import Inscripcion
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from inscripciones.serializers import InscripcionSerializer
from users.permissions import IsAdminOrSuperAdmin, IsProfesor

from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
    
)

from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo,
    Etapa,              
    ProgresoEstudiante,
    
)

from .serializers import (
    LaboratorioProfesorAdminSerializer,
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    ObjetivoSerializer,
    LaboratorioProfesorSerializer,
   
)


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class ObjetivoViewSet(ModelViewSet):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    permission_classes = [IsAuthenticated]


class PalabraClaveViewSet(ModelViewSet):
    queryset = PalabraClave.objects.all()
    serializer_class = PalabraClaveSerializer
    permission_classes = [IsAuthenticated]


class LaboratorioViewSet(ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [IsAuthenticated]

    # Filtros, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'objetivo', 'creador', 'estado']
    search_fields = ['titulo_lab', 'resumen', 'introduccion', 'marco_teorico']
    ordering_fields = ['titulo_lab', 'fecha_creacion', 'fecha_actualizacion']
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
            queryset = queryset.filter(titulo_lab__icontains=nombre)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)


    def get_permissions(self):
        if self.action == "cargar_estudiantes_excel":
            return [IsAuthenticated(), IsProfesor()]

        return [IsAuthenticated()]

# =========================================================
# LABORATORIO PROFESOR
# =========================================================
class LaboratorioProfesorViewSet(ModelViewSet):

    queryset = Laboratorio.objects.filter(
        id_padre__isnull=False
    )

    serializer_class = LaboratorioProfesorSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = [
        'profesor',
        'estado',
        'generado_ia'
    ]

    search_fields = [
        'codigo_lab',
        'titulo_lab'
    ]

    ordering_fields = [
        'fecha_creacion',
        'fecha_actualizacion'
    ]

    ordering = ['-fecha_creacion']

    def generar_codigo(self):

        while True:

            codigo = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=8
                )
            )

            if not Laboratorio.objects.filter(
                codigo_lab=codigo
            ).exists():

                return codigo
            
    def perform_create(self, serializer):

        laboratorio_base = serializer.validated_data['id_padre']

        nuevo_laboratorio = serializer.save(
            profesor=self.request.user,
            codigo_lab=self.generar_codigo(),

            titulo_lab=laboratorio_base.titulo_lab,
            categoria=laboratorio_base.categoria,
            objetivo=laboratorio_base.objetivo,
            creador=laboratorio_base.creador,

            resumen=laboratorio_base.resumen,
            prologo=laboratorio_base.prologo,
            introduccion=laboratorio_base.introduccion,
            marco_teorico=laboratorio_base.marco_teorico,
        )

    # Copiar palabras clave
        nuevo_laboratorio.palabras_clave.set(
            laboratorio_base.palabras_clave.all()
    )

    @action(detail=False, methods=['get'])
    def mis_laboratorios(self, request):
        qs = self.queryset.filter(profesor=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):

        laboratorio = self.get_object()

        inscripciones = Inscripcion.objects.filter(
            laboratorio=laboratorio
        )

        estudiantes = []

        for inscripcion in inscripciones:

            estudiantes.append({
                "id": inscripcion.usuario.id,
                "nombre": inscripcion.usuario.nombre,
                "correo": inscripcion.usuario.correo,
                "fecha_inscripcion": inscripcion.fecha_inscripcion
            })

        return Response(estudiantes)
    

    @action(detail=True, methods=['get'])
    def progreso(self, request, pk=None):
        laboratorio = self.get_object()
        etapas = Etapa.objects.filter(laboratorio=laboratorio).order_by('orden')
        total = etapas.count()
        completadas = 0
        resultado = []

        for etapa in etapas:
            prog = ProgresoEstudiante.objects.filter(
                estudiante=request.user, etapa=etapa
            ).first()
            hecho = prog.completada if prog else False
            if hecho:
                completadas += 1
            resultado.append({"etapa_id": etapa.id, "nombre": etapa.nombre, "completada": hecho})

        return Response({
            "porcentaje": int((completadas / total) * 100) if total > 0 else 0,
            "etapas": resultado
        })


    @action(detail=True, methods=['post'], url_path='etapas/(?P<etapa_id>[^/.]+)/completar')
    def completar_etapa(self, request, pk=None, etapa_id=None):
        laboratorio = self.get_object()
        try:
            etapa = Etapa.objects.get(id=etapa_id, laboratorio=laboratorio)
        except Etapa.DoesNotExist:
            return Response({"error": "Etapa no encontrada"}, status=404)

        prog, _ = ProgresoEstudiante.objects.get_or_create(
            estudiante=request.user, etapa=etapa
        )
        prog.completada = True
        prog.fecha_completado = date.today()
        prog.save()

        return Response({"mensaje": f"Etapa '{etapa.nombre}' completada ✅"})

    @action(detail=True, methods=['post'], url_path='cargar-estudiantes')
    def cargar_estudiantes_excel(self, request, pk=None):

        laboratorio = self.get_object()
        archivo = request.FILES.get('file')

        if not archivo:
            return Response({"error": "No se envió archivo"}, status=400)

        try:
            df = pd.read_excel(archivo)
        except:
            return Response({"error": "Archivo inválido"}, status=400)

        creados = 0
        errores = []

        with transaction.atomic():
            for index, row in df.iterrows():

                try:
                    usuario = Users.objects.get(correo=row['correo'])

                    if usuario.rol != "estudiante":
                        errores.append(f"Fila {index}: el usuario no es estudiante")
                        continue

                    inscripcion, created = Inscripcion.objects.get_or_create(
                        usuario=usuario,
                        laboratorio=laboratorio,
                        defaults={"fecha_inscripcion": date.today()}
                    )

                    if created:
                        creados += 1
                    else:
                        errores.append(f"Fila {index}: ya inscrito")

                except Users.DoesNotExist:
                    errores.append(f"Fila {index}: usuario no existe")

        return Response({
            "mensaje": "Inscripción finalizada",
            "creados": creados,
            "errores": errores
        })

# =========================================================
# LABORATORIOS PROFESOR
# =========================================================
class MisLaboratoriosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        usuario = request.user

        laboratorios = Laboratorio.objects.filter(
            profesor=usuario,
            id_padre__isnull=False
        ).order_by('-fecha_actualizacion')

        serializer = LaboratorioProfesorSerializer(
            laboratorios,
            many=True
        )

        return Response(serializer.data)

# =========================================================
# INSCRIBIR USUARIO POR CODIGO
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inscribir_usuario(request):

    codigo = request.data.get('codigo_lab')

    try:
        laboratorio = Laboratorio.objects.get(
            codigo_lab=codigo
        )

    except Laboratorio.DoesNotExist:

        return Response(
            {"error": "Código inválido"},
            status=404
        )

    existe = Inscripcion.objects.filter(
        usuario=request.user,
        laboratorio=laboratorio
    ).exists()

    if existe:

        return Response(
            {"error": "Ya estás inscrito en este laboratorio"},
            status=400
        )

    Inscripcion.objects.create(
        usuario=request.user,
        laboratorio=laboratorio,
        fecha_inscripcion=date.today()
    )

    return Response(
        {
            "mensaje": "Inscripción exitosa",
            "redirect_to": f"/laboratorio/{laboratorio.id}",
            "laboratorio": {
                "id": laboratorio.id,
                "titulo": laboratorio.titulo_lab,
                "codigo": laboratorio.codigo_lab
            }
        },
        status=201
    )

# =========================================================
# LABORATORIOS - ADMIN
# =========================================================
class LaboratorioAdminViewSet(ModelViewSet):
    serializer_class = LaboratorioProfesorAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get_queryset(self):
        return Laboratorio.objects.filter(
            id_padre__isnull=False
        ).order_by('-fecha_actualizacion')
