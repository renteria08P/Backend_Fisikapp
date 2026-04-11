from rest_framework import viewsets
from .models import Informe, Resultado, Conclusiones, Recomendaciones
from .serializers import (
    InformeSerializer,
    ResultadoSerializer,
    ConclusionesSerializer,
    RecomendacionesSerializer
)


class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer


class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer


class ConclusionesViewSet(viewsets.ModelViewSet):
    queryset = Conclusiones.objects.all()
    serializer_class = ConclusionesSerializer


class RecomendacionesViewSet(viewsets.ModelViewSet):
    queryset = Recomendaciones.objects.all()
    serializer_class = RecomendacionesSerializer
