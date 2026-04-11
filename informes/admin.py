from django.contrib import admin
from .models import Informe, Resultado, Conclusiones, Recomendaciones

admin.site.register(Informe)
admin.site.register(Resultado)
admin.site.register(Conclusiones)
admin.site.register(Recomendaciones)
