import random
import string
import os

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  filters
from rest_framework.decorators import action
from inscripciones.models import Inscripcion
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from inscripciones.serializers import InscripcionSerializer
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
    LaboratorioProfesor,
)

from .serializers import (
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    ObjetivoSerializer,
    LaboratorioProfesorSerializer
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
    filterset_fields = ['categoria', 'objetivo', 'creador', 'estado', 'ra']
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





# =========================================================
# LABORATORIO PROFESOR
# =========================================================

class LaboratorioProfesorViewSet(ModelViewSet):

    queryset = LaboratorioProfesor.objects.all()

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
        'laboratorio__titulo_lab'
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

            if not LaboratorioProfesor.objects.filter(
                codigo_lab=codigo
            ).exists():

                return codigo
            

    def perform_create(self, serializer):

        laboratorio = serializer.validated_data['laboratorio']

        serializer.save(
            profesor=self.request.user,
            codigo_lab=self.generar_codigo(),

            # COPIA AUTOMÁTICA
            resumen=laboratorio.resumen,
            prologo=laboratorio.prologo,
            introduccion=laboratorio.introduccion,
            marco_teorico=laboratorio.marco_teorico,
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
# =========================================================
# LABORATORIOS PROFESOR
# =========================================================
class MisLaboratoriosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        laboratorios = LaboratorioProfesor.objects.filter(
            profesor=usuario
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
        laboratorio = LaboratorioProfesor.objects.get(
            codigo_lab=codigo
        )

    except LaboratorioProfesor.DoesNotExist:

        return Response(
            {"error": "Código inválido"},
            status=404
        )

    # EVITAR INSCRIPCIONES DUPLICADAS
    existe = Inscripcion.objects.filter(
        usuario=request.user,
        laboratorio=laboratorio
    ).exists()

    if existe:

        return Response(
            {"error": "Ya estás inscrito en este laboratorio"},
            status=400
        )

    inscripcion = Inscripcion.objects.create(
        usuario=request.user,
        laboratorio=laboratorio,
        fecha_inscripcion=date.today()
    )

    serializer = InscripcionSerializer(inscripcion)

    return Response(serializer.data, status=201)