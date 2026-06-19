from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.conf import settings


# =========================================================
# CONCEPTOS BASICOS
# =========================================================
class ConceptosBasicos(models.Model):
    descripcion = models.TextField()
    concepto = models.CharField(max_length=100)
    ejemplo = models.TextField()
    tipo = models.CharField(max_length=50)

    recursos = models.ManyToManyField(
        'Recursos',
        blank=True
    )

    def __str__(self):
        return self.concepto


    class Meta:
        ordering = ['concepto']
    
# =========================================================
# RECURSOS
# =========================================================
class Recursos(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    archivo = models.FileField(
        upload_to='recursos/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf',
                    'doc',
                    'docx'
                ]
            )
        ]
    )

    url = models.URLField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre
    
# =========================================================
# PLANTILLA PRACTICA
# =========================================================

class PlantillaPractica(models.Model):

    plantilla = models.ForeignKey(
        'laboratorios.PlantillaLaboratorio',
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
        related_name='practicas_plantilla'
    )

    def __str__(self):
        return self.nombre_practica
    
    class Meta:
        ordering = ['nombre_practica']


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

# =========================================================
# PLANTILLA PROCEDIMIENTO
# =========================================================
class PlantillaProcedimiento(models.Model):

    plantilla = models.ForeignKey(
        'laboratorios.PlantillaLaboratorio',
        on_delete=models.CASCADE,
        related_name='procedimientos'
    )

    muestras = models.TextField()

    calculos = models.TextField()

    resultados = models.TextField()

    def __str__(self):
        return f"Procedimiento {self.id}"


class Procedimiento(models.Model):

    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        on_delete=models.CASCADE,
        related_name='procedimientos'
    )

    muestras = models.TextField()

    calculos = models.TextField()

    resultados = models.TextField()

    def __str__(self):
        return f"Procedimiento {self.id}"

# =========================================================
# PLANTILLA FORMULAS
# =========================================================
class PlantillaFormula(models.Model):

    plantilla = models.ForeignKey(
        'laboratorios.PlantillaLaboratorio',
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

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='activo'
    )

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
