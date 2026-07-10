from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from cloudinary.models import CloudinaryField

# =========================================================
# CONCEPTOS BASICOS
# =========================================================
class ConceptosBasicos(models.Model):
    descripcion = models.TextField()
    concepto = models.CharField(max_length=100)
    ejemplo = models.TextField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.concepto

    class Meta:
        ordering = ['concepto']

# =========================================================
# CONCEPTO LABORATORIO
# =========================================================
class ConceptoLaboratorio(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='conceptos_laboratorio'
    )

    concepto_original = models.ForeignKey(
        ConceptosBasicos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="conceptos_originales"
    )

    concepto = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    ejemplo = models.TextField()

    tipo = models.CharField(
        max_length=50
    )

    recursos = models.ManyToManyField(
        'Recursos',
        blank=True,
        related_name='conceptos_laboratorio'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['laboratorio', 'concepto_original'],
                name='unique_concepto_laboratorio'
            )
        ]

    def __str__(self):
        return f"{self.laboratorio} - {self.concepto}"
    
# =========================================================
# RECURSOS
# =========================================================
class Recursos(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    url = models.URLField(
        null=True,
        blank=True
    )

    archivo = CloudinaryField(
        resource_type="raw",
        folder="recursos",
        blank=True,
        null=True
    )

    def clean(self):
        if not self.url and not self.archivo:
            raise ValidationError(
                "Debe registrar una URL o un archivo."
            )

    def __str__(self):
        return self.nombre
    

class Practica(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='practicas'
    )

    nombre_practica = models.CharField(
        max_length=100
    )

    objetivo = models.TextField()

    descripcion = models.TextField()

    materiales = models.TextField()

    calculos = models.TextField()

    conceptos = models.ManyToManyField(
        ConceptosBasicos,
        blank=True,
        related_name='practicas'
    )

    def __str__(self):
        return self.nombre_practica
    
    class Meta:
        ordering = ['nombre_practica']


class Procedimiento(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='procedimientos'
    )

    paso_numero = models.PositiveSmallIntegerField()
    descripcion = models.TextField()
    imagen = CloudinaryField(
        "image",
        folder="procedimientos",
        null=True,
        blank=True
    )
    orden = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Paso {self.paso_numero}"


class Formula(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='formulas'
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    expresion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
    
# =========================================================
# PRACTICA ESTUDIANTE
# =========================================================
class PracticaEstudiante(models.Model):

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    practica = models.ForeignKey(
        Practica,
        on_delete=models.CASCADE,
        related_name='practicas_estudiantes'
    )

    fecha_inicio = models.DateTimeField(
        auto_now_add=True
    )

    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = (
            'estudiante',
            'practica'
        )

    def __str__(self):
        return f"{self.estudiante} - {self.practica.nombre_practica}"
