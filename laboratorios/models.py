from django.db import models
from django.conf import settings


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Objetivo(models.Model):
    tipo_objetivo = models.CharField(max_length=100)
    descripcion_objetivo = models.TextField()

    def __str__(self):
        return self.tipo_objetivo


class PalabraClave(models.Model):
    palabra_clave = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return self.palabra_clave


class Laboratorio(models.Model):
    titulo_lab = models.CharField(max_length=200)
    codigo_lab = models.CharField(max_length=50, unique=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='laboratorios_creados')
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE)

    palabras_clave = models.ManyToManyField(PalabraClave)

    resumen = models.TextField()
    prologo = models.TextField(null=True, blank=True)
    introduccion = models.TextField()
    marco_teorico = models.TextField()

    estado = models.BooleanField(default=True)
    ra = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo_lab