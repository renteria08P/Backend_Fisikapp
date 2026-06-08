from django.db import models
from django.conf import settings


# =========================================================
# CATEGORIA
# =========================================================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# =========================================================
# OBJETIVOS
# =========================================================

class ObjetivoGeneral(models.Model):

    laboratorio = models.OneToOneField(
        'Laboratorio',
        on_delete=models.CASCADE,
        related_name="objetivo_general"
    )

    def __str__(self):
        return self.descripcion[:50]

    descripcion = models.TextField()
    

class ObjetivoEspecifico(models.Model):

    objetivo_general = models.ForeignKey(
        ObjetivoGeneral,
        on_delete=models.CASCADE,
        related_name="objetivos_especificos"
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion


# =========================================================
# PALABRAS CLAVES
# =========================================================
class PalabraClave(models.Model):
    palabra_clave = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return self.palabra_clave
    

# =========================================================
# LABORATORIO BASE
# =========================================================

class Laboratorio(models.Model):

    titulo_lab = models.CharField(max_length=200)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='laboratorios_creados'
    )


    palabras_clave = models.ManyToManyField(
        PalabraClave
    )

    conceptos_basicos = models.ManyToManyField(
        'contenido.ConceptosBasicos',
        blank=True
    )

    resumen = models.TextField()

    prologo = models.TextField(
        null=True,
        blank=True
    )

    introduccion = models.TextField()

    marco_teorico = models.TextField()

    estado = models.BooleanField(default=True)

    # =====================================
    # NUEVOS CAMPOS PARA RELACIÓN REFLEXIVA
    # =====================================

    id_padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='copias'
    )

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='laboratorios_asignados'
    )

    codigo_lab = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        default=None
    )

    grado = models.CharField(
        max_length=25,
        null=True,
        blank=True
    )

    jornada = models.CharField(
        max_length=25,
        null=True,
        blank=True
    )

    simulacion = models.BooleanField(
        default=False
    )

    generado_ia = models.BooleanField(
        default=False
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.titulo_lab

# =========================================================
# ETAPAS DEL LABORATORIO
# =========================================================
class Etapa(models.Model):
    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.CASCADE,
        related_name='etapas'
    )
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()

    def __str__(self):
        return f"{self.orden}. {self.nombre}"


# =========================================================
# PROGRESO DEL ESTUDIANTE
# =========================================================
class ProgresoEstudiante(models.Model):
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    etapa = models.ForeignKey(
        Etapa,
        on_delete=models.CASCADE
    )
    completada = models.BooleanField(default=False)
    fecha_completado = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['estudiante', 'etapa']

    def __str__(self):
        return f"{self.estudiante} - {self.etapa}"
    
