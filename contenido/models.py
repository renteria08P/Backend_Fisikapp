from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# IMPORTANTE: usamos string para evitar errores de import entre apps

class ConceptosBasicos(models.Model):
    descripcion = models.TextField()
    concepto = models.CharField(max_length=100)
    ejemplo = models.TextField()
    tipo = models.CharField(max_length=50)
    fecha = models.DateField()

    recursos = models.ManyToManyField('Recursos', blank=True)


    def __str__(self):
        return self.concepto
    
class Recursos(models.Model):
    nombre = models.CharField(max_length=100, blank=True)

    archivo = models.FileField(
        upload_to='recursos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )

    url = models.URLField(
        null=True,
        blank=True
    )

    def clean(self):
        if not self.archivo and not self.url:
            raise ValidationError("Debes subir un archivo o proporcionar una URL.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recurso {self.id}"
    

class Practicas(models.Model):
    nombre_practica = models.CharField(max_length=100)
    concepto = models.CharField(max_length=100)
    objetivo = models.TextField()
    descripcion = models.TextField()
    materiales = models.TextField()
    calculos = models.TextField()
    laboratorio = models.ForeignKey('laboratorios.Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_practica


class Procedimientos(models.Model):
    laboratorio = models.ForeignKey('laboratorios.Laboratorio', on_delete=models.CASCADE)
    muestras = models.TextField()
    calculos = models.TextField()
    resultados = models.TextField()

    def __str__(self):
        return f"Procedimiento {self.id}"


class Formulas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    expresion = models.TextField()
    laboratorio = models.ForeignKey('laboratorios.Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Bibliografia(models.Model):
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    tipo_fuente = models.CharField(max_length=100)
    anio = models.IntegerField()
    editorial = models.CharField(max_length=150)
    url = models.URLField()
    fecha_consulta = models.DateField()
    descripcion = models.TextField()
    laboratorio = models.ForeignKey('laboratorios.Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
