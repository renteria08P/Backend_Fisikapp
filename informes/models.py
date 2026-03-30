from django.db import models

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)

class Conclusiones(models.Model):
    descripcion = models.TextField()

class Recomendaciones(models.Model):
    descripcion = models.TextField()

class Informe(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    desarrollo = models.TextField()
    resultado = models.TextField()
    analisis = models.TextField()
    conclusiones = models.ForeignKey(Conclusiones, on_delete=models.CASCADE)
    recomendaciones = models.ForeignKey(Recomendaciones, on_delete=models.CASCADE)
    autor = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)