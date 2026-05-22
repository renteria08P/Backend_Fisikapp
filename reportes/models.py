from django.db import models
from django.conf import settings

from laboratorios.models import LaboratorioProfesor


class ReporteLaboratorio(models.Model):

    ESTADOS = (
        ('Generado', 'Generado'),
        ('Pendiente', 'Pendiente'),
    )

    laboratorio_profesor = models.ForeignKey(
        LaboratorioProfesor,
        on_delete=models.CASCADE,
        related_name='reportes'
    )

    estudiantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='reportes_estudiante'
    )

    estado_informe = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Generado'
    )

    fecha_creacion = models.DateField(
        auto_now_add=True
    )

    # PDF subido estudiantes
    reporte_estudiante = models.FileField(
        upload_to='reportes/estudiantes/',
        null=True,
        blank=True
    )

    # observaciones del docente
    observaciones_docente = models.TextField(
        null=True,
        blank=True
    )

    # PDF final
    informe_final = models.FileField(
        upload_to='reportes/finales/',
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.laboratorio_profesor.codigo_lab}"