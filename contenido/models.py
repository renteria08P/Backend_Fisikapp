from django.db import models

# Create your models here.

from django.db import models

# IMPORTANTE: usamos string para evitar errores de import entre apps

class ConceptosBasicos(models.Model):
    descripcion = models.TextField()
    concepto = models.CharField(max_length=100)
    ejemplo = models.TextField()
    tipo = models.CharField(max_length=50)
    fecha = models.DateField()

    def __str__(self):
        return self.concepto


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
