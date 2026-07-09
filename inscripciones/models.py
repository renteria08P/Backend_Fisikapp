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
        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "asignacion"],
                name="unique_estudiante_asignacion"
            )
        ]
        ordering = ["-fecha_inscripcion"]

class GrupoEstudiante(models.Model):

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grupos_estudiante"
    )

    grupo = models.ForeignKey(
        "laboratorios.GrupoAcademico",
        on_delete=models.CASCADE,
        related_name="estudiantes_inscritos"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="ACTIVO"
    )

    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "grupo"],
                name="unique_estudiante_grupo"
            )
        ]
        ordering = ["-fecha_inscripcion"]

    def __str__(self):
        return f"{self.estudiante} - {self.grupo.nombre}"