from django.db import models
from django.conf import settings


class Log(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    accion = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return f"{self.usuario} - {self.accion}"


class Notificacion(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )

    titulo = models.CharField(
        max_length=200
    )

    mensaje = models.TextField()

    leida = models.BooleanField(
        default=False
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_creacion']