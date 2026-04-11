from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo
)

from .serializers import (
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    ObjetivoSerializer
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

    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)

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