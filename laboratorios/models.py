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

class Objetivo(models.Model):
    tipo_objetivo = models.CharField(max_length=100)
    descripcion_objetivo = models.TextField()

    def __str__(self):
        return self.tipo_objetivo


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

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='laboratorios_creados')
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE)

    palabras_clave = models.ManyToManyField(PalabraClave)

    resumen = models.TextField()
    prologo = models.TextField(null=True, blank=True)
    introduccion = models.TextField()
    marco_teorico = models.TextField()

    estado = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo_lab


# =========================================================
# LABORATORIO PROFESOR -- CON CODIGO
# =========================================================

class LaboratorioProfesor(models.Model):

    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.CASCADE,
        related_name='profesores'
    )

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='laboratorios_profesor'
    )

    codigo_lab = models.CharField(
        max_length=10,
        unique=True
    )

    # COPIA EDITABLE
    resumen = models.TextField()

    prologo = models.TextField(
        null=True,
        blank=True
    )

    introduccion = models.TextField()

    marco_teorico = models.TextField()

    recursos = models.ManyToManyField(
        'contenido.Recursos',
        blank=True
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

    generado_ia = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    simulacion = models.BooleanField(default=False)


    

# =========================================================
# ETAPAS DEL LABORATORIO
# =========================================================
class Etapa(models.Model):
    laboratorio = models.ForeignKey(
        LaboratorioProfesor,
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
    


# =========================================================
# ACTIVIDAD LABORATORIO (GENERADA POR IA)
# =========================================================
class ActividadLaboratorio(models.Model):

    NIVELES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]

    laboratorio = models.ForeignKey(
        LaboratorioProfesor,
        on_delete=models.CASCADE,
        related_name='actividades'
    )
    nivel = models.CharField(max_length=20, choices=NIVELES)
    descripcion = models.TextField()
    generado_ia = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.laboratorio} - {self.nivel}"


# =========================================================
# DETALLE ACTIVIDAD (GENERADA POR IA)
# =========================================================
class DetalleActividad(models.Model):

    actividad = models.OneToOneField(
        ActividadLaboratorio,
        on_delete=models.CASCADE,
        related_name='detalle'
    )
    objetivo_especifico = models.TextField()
    materiales = models.JSONField()
    procedimiento = models.JSONField()
    formula = models.TextField(blank=True, null=True)
    tiempo_estimado = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detalle de {self.actividad}"