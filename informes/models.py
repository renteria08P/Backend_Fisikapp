from django.db import models
from users.models import Users
from laboratorios.models import Laboratorio

class Informe(models.Model):
    estudiante = models.ForeignKey(Users, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class Resultado(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE)
    descripcion = models.TextField()

class Conclusiones(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE)
    descripcion = models.TextField()

class Recomendaciones(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE)
    descripcion = models.TextField()