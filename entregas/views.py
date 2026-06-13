from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import  ( 
    Pregunta,
    Respuesta,
    Entrega, 
    ResultadoPractica,
    ResultadoSimulacion
)

from .serializers import (
    ResultadoPracticaSerializer,
    EntregaSerializer,
    PreguntaSerializer,
    RespuestaSerializer,
    ResultadoSimulacionSerializer
)


class PreguntaViewSet(ModelViewSet):

    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [IsAuthenticated]


class RespuestaViewSet(ModelViewSet):

    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    permission_classes = [IsAuthenticated]


class EntregaViewSet(ModelViewSet):

    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [IsAuthenticated]


class ResultadoPracticaViewSet(
    ModelViewSet
):

    queryset = ResultadoPractica.objects.all()

    serializer_class = (
        ResultadoPracticaSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class ResultadoSimulacionViewSet(
    ModelViewSet
):

    queryset = ResultadoSimulacion.objects.all()

    serializer_class = (
        ResultadoSimulacionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]