from django.db import models
from users.models import Users

class Notificacion(models.Model):
    usuario = models.ForeignKey(Users, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)