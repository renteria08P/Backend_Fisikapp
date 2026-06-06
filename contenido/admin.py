from django.contrib import admin
from .models import ConceptosBasicos, Practicas, Procedimientos, Formulas, Bibliografia

admin.site.register(ConceptosBasicos)
admin.site.register(Practicas)
admin.site.register(Procedimientos)
admin.site.register(Formulas)
admin.site.register(Bibliografia)
