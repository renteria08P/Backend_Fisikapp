from django.db import models


# =========================================================
# LECTURA ESTUDIANTE
# =========================================================

class LecturaEstudiante(models.Model):

    SECCIONES = (
        ('PROLOGO', 'Prólogo'),
        ('INTRODUCCION', 'Introducción'),
        ('MARCO_TEORICO', 'Marco Teórico'),
        ('CONCEPTOS_BASICOS', 'Conceptos Básicos'),
    )

    entrega = models.ForeignKey(
        'entregas.Entrega',
        on_delete=models.CASCADE,
        related_name='lecturas'
    )

    seccion = models.CharField(
        max_length=30,
        choices=SECCIONES
    )

    leido = models.BooleanField(
        default=False
    )

    fecha_lectura = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'entrega',
            'seccion'
        )
        ordering = ['fecha_lectura']

    def __str__(self):
        return (
            f"{self.entrega.inscripcion.estudiante} - "
            f"{self.seccion}"
        )