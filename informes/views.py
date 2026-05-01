from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Informe, Resultado, Conclusiones, Recomendaciones
from .serializers import (
    InformeSerializer,
    ResultadoSerializer,
    ConclusionesSerializer,
    RecomendacionesSerializer
)

# =========================
# INFORME
# =========================
class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['laboratorio', 'autor', 'fecha']
    search_fields = ['desarrollo', 'analisis']
    ordering_fields = ['fecha']
    ordering = ['fecha']

# =========================
# RESULTADOS
# =========================
class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['informe', 'instrumento']
    search_fields = ['observaciones']
    ordering_fields = ['fecha', 'valor']
    ordering = ['fecha']

# =========================
# CONCLUSIONES
# =========================
class ConclusionesViewSet(viewsets.ModelViewSet):
    queryset = Conclusiones.objects.all()
    serializer_class = ConclusionesSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['informe', 'importancia']
    search_fields = ['descripcion']
    ordering_fields = ['fecha']
    ordering = ['fecha']

# =========================
# RECOMENDACIONES
# =========================
class RecomendacionesViewSet(viewsets.ModelViewSet):
    queryset = Recomendaciones.objects.all()
    serializer_class = RecomendacionesSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['informe', 'prioridad']
    search_fields = ['descripcion']
    ordering_fields = ['fecha']
    ordering = ['fecha']
