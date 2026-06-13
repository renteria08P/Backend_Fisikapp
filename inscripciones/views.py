from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inscripcion
from .serializers import InscripcionSerializer
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes  
from laboratorios.models import Asignacion

class InscripcionesViewSet(viewsets.ModelViewSet):

    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = [
        'estudiante',
        'asignacion',
        'fecha_inscripcion'
    ]

    ordering_fields = [
        'fecha_inscripcion'
    ]

    @swagger_auto_schema(
        operation_summary="Listar inscripciones",
        operation_description="""
        Retorna todas las inscripciones registradas.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalle de inscripción",
        operation_description="""
        Retorna la información de una inscripción específica.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inscribir_usuario(request):

    codigo = request.data.get('codigo')

    if not codigo:
        return Response(
            {"error": "Debe enviar el código"},
            status=400
        )

    try:

        asignacion = Asignacion.objects.get(
            codigo_ingreso=codigo
        )

    except Asignacion.DoesNotExist:

        return Response(
            {"error": "Código inválido"},
            status=404
        )

    existe = Inscripcion.objects.filter(
        estudiante=request.user,
        asignacion=asignacion
    ).exists()

    if existe:

        return Response(
            {"error": "Ya estás inscrito"},
            status=400
        )

    inscripcion = Inscripcion.objects.create(
        estudiante=request.user,
        asignacion=asignacion
    )

    serializer = InscripcionSerializer(inscripcion)

    return Response(
        serializer.data,
        status=201
    )

@api_view(['GET'])
def listar_inscripciones(request):
    inscripciones = Inscripcion.objects.all()
    serializer = InscripcionSerializer(inscripciones, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='put', request_body=InscripcionSerializer)
@api_view(['PUT', 'DELETE'])
def detalle_inscripcion(request, pk):
    try:
        inscripcion = Inscripcion.objects.get(pk=pk)
    except Inscripcion.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = InscripcionSerializer(inscripcion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        inscripcion.delete()
        return Response({"mensaje": "Eliminado correctamente"}, status=204)
    
# =============================================
#  MIS LABORATORIOS ESTUDIANTE
# =============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_laboratorios(request):

    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user
    )
    serializer = InscripcionSerializer(inscripciones, many=True)
    return Response(serializer.data)

