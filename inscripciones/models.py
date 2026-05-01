from django.db import models
from django.conf import settings

class Inscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey('laboratorios.Laboratorio', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'laboratorio'], name='unique_usuario_laboratorio')
        ]

    def __str__(self):
        return f"{self.usuario} - {self.laboratorio}"
    

