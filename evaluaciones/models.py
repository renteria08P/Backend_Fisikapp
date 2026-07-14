from django.db import models
from django.conf import settings


# =========================================================
# EVALUACION IA
# =========================================================

class EvaluacionIA(models.Model):

    entrega = models.OneToOneField(
        'entregas.Entrega',
        on_delete=models.CASCADE,
        related_name='evaluacion_ia'
    )

    calificacion = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    retroalimentacion = models.TextField()

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    fecha_evaluacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"IA - Entrega {self.entrega.id}"
        )

    class Meta:
        ordering = ['-fecha_evaluacion']
        
# =========================================================
# EVALUACION DOCENTE
# =========================================================

class EvaluacionProfesor(models.Model):

    entrega = models.OneToOneField(
        'entregas.Entrega',
        on_delete=models.CASCADE,
        related_name='evaluacion_docente'
    )

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evaluaciones_docente'
    )

    calificacion = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    comentarios = models.TextField(
        blank=True,
        null=True
    )

    fecha_evaluacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Docente - Entrega {self.entrega.id}"
        )

    class Meta:
        ordering = ['-fecha_evaluacion']