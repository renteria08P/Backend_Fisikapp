from django.db import models

class Users(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    identificacion = models.CharField(max_length=20, unique=True)    
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    institucion = models.CharField(max_length=100)
    rol = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre