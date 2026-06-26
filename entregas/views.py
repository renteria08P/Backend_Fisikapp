from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsProfesor
from rest_framework.exceptions import ValidationError
from users.permissions import Roles


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

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]

class RespuestaViewSet(ModelViewSet):

    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    
    def get_permissions(self):

        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]
    
    def perform_create(self, serializer):

        entrega = serializer.validated_data["entrega"]

        if entrega.inscripcion.estudiante != self.request.user:
            raise ValidationError(
                "No puedes responder otra entrega."
            )

        serializer.save()


    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return Respuesta.objects.filter(
                entrega__inscripcion__estudiante=self.request.user
            )

        return Respuesta.objects.all()


class EntregaViewSet(ModelViewSet):

    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer

    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return Entrega.objects.filter(
                inscripcion__estudiante=self.request.user
            )

        return Entrega.objects.all()
    
    def get_permissions(self):

        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]
    
    def perform_create(self, serializer):

        inscripcion = serializer.validated_data["inscripcion"]

        if inscripcion.estudiante != self.request.user:
            raise ValidationError(
                "No puedes crear entregas para otro estudiante."
            )

        serializer.save()


class ResultadoPracticaViewSet(
    ModelViewSet
):

    queryset = ResultadoPractica.objects.all()

    serializer_class = (
        ResultadoPracticaSerializer
    )

    def get_permissions(self):

        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]
    
    def perform_create(self, serializer):

        entrega = serializer.validated_data["entrega"]

        if entrega.inscripcion.estudiante != self.request.user:
            raise ValidationError(
                "No puedes registrar resultados de otra entrega."
            )

        serializer.save()

    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return ResultadoPractica.objects.filter(
                entrega__inscripcion__estudiante=self.request.user
            )

        return ResultadoPractica.objects.all()


class ResultadoSimulacionViewSet(
    ModelViewSet
):

    queryset = ResultadoSimulacion.objects.all()

    serializer_class = (
        ResultadoSimulacionSerializer
    )

    def get_permissions(self):

        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]
    
    def perform_create(self, serializer):

        entrega = serializer.validated_data["entrega"]

        if entrega.inscripcion.estudiante != self.request.user:
            raise ValidationError(
                "No puedes registrar resultados de otra entrega."
            )

        serializer.save()

    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return ResultadoSimulacion.objects.filter(
                entrega__inscripcion__estudiante=self.request.user
            )

        return ResultadoSimulacion.objects.all()