from django.db import models
from django.conf import settings
from laboratorios.models import Laboratorio

#Informe
class Informe(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    desarrollo = models.TextField()
    analisis = models.TextField()
    conclusiones = models.TextField()
    recomendaciones = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Informe {self.id} - {self.laboratorio}"

#Resultado
class Resultado(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='resultados')
    valor = models.FloatField()
    unidad = models.CharField(max_length=50)
    instrumento = models.CharField(max_length=100)
    observaciones = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Resultado {self.id} - Informe {self.informe.id}"
    
#Conclisiones
class Conclusiones(models.Model):
    informe = models.ForeignKey(
        Informe,
        on_delete=models.CASCADE,
        related_name='conclusiones'
    )
    descripcion = models.TextField()
    importancia = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Conclusion {self.id}"
    
#Recomendaciones
class Recomendaciones(models.Model):
    informe = models.ForeignKey(
        Informe,
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Recomendacion {self.id}"