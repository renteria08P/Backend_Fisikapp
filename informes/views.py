from django.shortcuts import render
from rest_framework import viewsets
from .models import Informe
from .serializers import InformeSerializer

# Create your views here.
class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer