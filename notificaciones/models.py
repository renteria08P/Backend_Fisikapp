from django.db import models
from django.conf import settings


class Log(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return f"{self.usuario} - {self.accion}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    estado = models.BooleanField(default=False)  # False = no leída
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"{self.usuario} - {'Leída' if self.estado else 'No leída'}"