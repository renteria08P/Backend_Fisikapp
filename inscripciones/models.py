from django.db import models

# Create your models here.

from django.db import models

class Inscripcion(models.Model):
    usuario_id = models.IntegerField()
    laboratorio_id = models.IntegerField()
    fecha_inscripcion = models.DateField()

    def __str__(self):
        return f"Usuario {self.usuario_id} - Lab {self.laboratorio_id}"
    

#  Tabla Conceptos Básicos
class ConceptosBasicos(models.Model):
    descripcion = models.TextField()
    concepto = models.CharField(max_length=100)
    ejemplo = models.TextField()
    tipo = models.CharField(max_length=50)
    fecha = models.DateField()

    def __str__(self):
        return self.concepto


# Tabla Prácticas
class Practicas(models.Model):
    nombre_practica = models.CharField(max_length=100)
    concepto = models.CharField(max_length=100)
    objetivo = models.TextField()
    descripcion = models.TextField()
    materiales = models.TextField()
    calculos = models.TextField()

    def __str__(self):
        return self.nombre_practica


# Tabla Procedimientos
class Procedimientos(models.Model):
    laboratorio_id = models.IntegerField()  # FK temporal
    muestras = models.TextField()
    calculos = models.TextField()
    resultados = models.TextField()

    def __str__(self):
        return f"Procedimiento {self.id}"
