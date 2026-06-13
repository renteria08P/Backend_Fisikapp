from django.db import models
from django.conf import settings


class Inscripcion(models.Model):

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    asignacion = models.ForeignKey(
        'laboratorios.Asignacion',
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return (
            f"{self.estudiante} - "
            f"{self.asignacion.laboratorio.titulo}"
        )

    class Meta:
        unique_together = (
            'estudiante',
            'asignacion'
        )
        ordering = ['-fecha_inscripcion']