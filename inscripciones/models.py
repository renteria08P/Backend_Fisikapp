from django.db import models
from users.models import Users
from laboratorios.models import Laboratorio

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Users, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.laboratorio}"