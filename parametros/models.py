from django.db import models


class Parametro(models.Model):
    clave = models.CharField(max_length=100, unique=True)
    valor = models.CharField(max_length=255)

    def clean(self):
        if self.clave == "MAX_INTENTOS_LOGIN" and not self.valor.isdigit():
            raise ValidationError("El valor debe ser un número entero.")

    def __str__(self):
        return f"{self.clave} = {self.valor}"