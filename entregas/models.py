from django.db import models
from django.core.exceptions import ValidationError


# =========================================================
# ENTREGAS
# =========================================================

class Entrega(models.Model):

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    inscripcion = models.OneToOneField(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='entrega'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVO'
    )

    fecha_inicio = models.DateTimeField(
        auto_now_add=True
    )

    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-fecha_creacion']


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.inscripcion.estudiante} - "
            f"{self.inscripcion.asignacion.laboratorio.titulo}"
        )

# =========================================================
# RESULTADOS PRACTICA
# =========================================================

class ResultadoPractica(models.Model):

    entrega = models.OneToOneField(
        Entrega,
        on_delete=models.CASCADE,
        related_name='resultado_practica'
    )

    observaciones = models.TextField()

    datos_obtenidos = models.TextField()

    conclusiones = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Resultado práctica "
            f"{self.entrega.id}"
        )


# =========================================================
# RESULTADO SIMULACION
# =========================================================

class ResultadoSimulacion(models.Model):

    entrega = models.OneToOneField(
        Entrega,
        on_delete=models.CASCADE,
        related_name='resultado_simulacion'
    )

    parametros = models.JSONField(
        null=True,
        blank=True
    )

    resultados = models.JSONField(
        null=True,
        blank=True
    )

    conclusiones = models.TextField(
        blank=True,
        null=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Simulación "
            f"{self.entrega.id}"
        )


# =========================================================
# PREGUNTAS
# =========================================================

class Pregunta(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='preguntas'
    )

    enunciado = models.TextField()

    orden = models.PositiveSmallIntegerField()

    obligatoria = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Pregunta {self.orden}"

    class Meta:
        ordering = ['orden']
        unique_together = (
            'laboratorio',
            'orden'
        )


# =========================================================
# RESPUESTAS
# =========================================================

class Respuesta(models.Model):

    entrega = models.ForeignKey(
        Entrega,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )

    respuesta = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            'entrega',
            'pregunta'
        )

    def __str__(self):
        return (
            f"Entrega {self.entrega.id} - "
            f"Pregunta {self.pregunta.id}"
        )