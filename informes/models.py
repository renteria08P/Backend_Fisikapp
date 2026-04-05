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

class Resultado(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='resultados')
    valor = models.FloatField()
    unidad = models.CharField(max_length=50)
    instrumento = models.CharField(max_length=100)
    observaciones = models.TextField()
    fecha = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Resultado {self.id} - Informe{self.informe.id}"