from django.db import models

# Create your models here.



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
from django.db import models
from users.models import Users
from laboratorios.models import Laboratorio

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Users, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.laboratorio}"
    
#Tabla Formulas

class Formulas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    expresion = models.TextField()

    def __str__(self):
        return self.nombre
    
#Tabla Bibliografia


class Bibliografia(models.Model):
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    tipo_fuente = models.CharField(max_length=100)
    anio = models.IntegerField()
    editorial = models.CharField(max_length=150)
    url = models.URLField()
    fecha_consulta = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo