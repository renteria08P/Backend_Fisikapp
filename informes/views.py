from django.shortcuts import render
from rest_framework import viewsets
from .models import Informe
from .models import Resultado
from .serializers import InformeSerializer
from .serializers import ResultadoSerializer

# Create your views here.
class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer