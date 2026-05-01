from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Inscripcion
from .serializers import InscripcionSerializer
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Inscripcion
from .serializers import InscripcionSerializer

class InscripcionesViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['usuario', 'laboratorio', 'fecha_inscripcion']
    ordering_fields = ['fecha_inscripcion']


@swagger_auto_schema(
    method='post',
    request_body=InscripcionSerializer
)

@api_view(['POST'])
def inscribir_usuario(request):
    serializer = InscripcionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

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

