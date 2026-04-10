from django.db import models
from laboratorios.models import Laboratorio
from django.conf import settings


class Informe(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    desarrollo = models.TextField()
    analisis = models.TextField()
    conclusiones = models.TextField()
    recomendaciones = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)