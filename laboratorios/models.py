from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import uuid

# =========================================================
# CATEGORIA
# =========================================================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nombre
    
    def clean(self):

        existe = Categoria.objects.filter(
            nombre__iexact=self.nombre.strip()
        ).exclude(
            pk=self.pk
        )

        if existe.exists():
            raise ValidationError({
                "nombre":
                "Ya existe una categoría con este nombre."
            })
        

    def save(self, *args, **kwargs):

        self.nombre = " ".join(
            self.nombre.strip().split()
        )

        self.full_clean()

        super().save(*args, **kwargs)


# =========================================================
# PLANTILLA DE LABORATORIO (ADMIN)
# =========================================================
class PlantillaLaboratorio(models.Model):

    resumen = models.TextField()

    introduccion = models.TextField()

    marco_teorico = models.TextField()

    imagen_portada = CloudinaryField(
        "image",
        folder="laboratorios/portadas",
        null=True,
        blank=True
    )

    conceptos_basicos = models.ManyToManyField(
        'contenido.ConceptosBasicos',
        blank=True,
        related_name='plantillas'
    )

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    titulo = models.CharField(
        max_length=200,
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='plantillas'
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plantillas_creadas'
    )

    lab_key = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVO'
    )

    descripcion = models.CharField(
        max_length=300,
        blank=True,
        default=""
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.titulo


    def clean(self):

        existe = PlantillaLaboratorio.objects.filter(
            titulo__iexact=self.titulo.strip()
        ).exclude(
            pk=self.pk
        )

        if existe.exists():
            raise ValidationError({
                "titulo":
                "Ya existe un laboratorio con este título."
            })


    def save(self, *args, **kwargs):

        self.titulo = " ".join(
            self.titulo.strip().split()
        )

        self.full_clean()

        super().save(*args, **kwargs)
    
# =========================================================
# LABORATORIO DEL PROFESOR
# =========================================================
class Laboratorio(models.Model):

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),   
        
    )

    plantilla = models.ForeignKey(
        PlantillaLaboratorio,
        on_delete=models.CASCADE,
        related_name='laboratorios'
    )

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='laboratorios'
    )

    resumen = models.TextField()

    introduccion = models.TextField()

    marco_teorico = models.TextField()

    generado_ia = models.BooleanField(
        default=False
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVO'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    @property
    def titulo(self):
        return self.plantilla.titulo

    @property
    def categoria(self):
        return self.plantilla.categoria

    def __str__(self):
        return f"{self.plantilla.titulo} - {self.profesor.nombre}"
    
    class Meta:
        ordering = ['-fecha_creacion']

class ObjetivoGeneral(models.Model):

    laboratorio = models.OneToOneField(
        Laboratorio,
        on_delete=models.CASCADE,
        related_name='objetivo_general'
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion[:50]

class ObjetivoEspecifico(models.Model):

    objetivo_general = models.ForeignKey(
        ObjetivoGeneral,
        on_delete=models.CASCADE,
        related_name='objetivos_especificos'
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

# =========================================================
# OBJETIVO GENERAL PLANTILLA
# =========================================================
class PlantillaObjetivoGeneral(models.Model):

    plantilla = models.OneToOneField(
        PlantillaLaboratorio,
        on_delete=models.CASCADE,
        related_name='objetivo_general'
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion[:50]


# =========================================================
# OBJETIVOS ESPECIFICOS PLANTILLA
# =========================================================
class PlantillaObjetivoEspecifico(models.Model):

    objetivo_general = models.ForeignKey(
        PlantillaObjetivoGeneral,
        on_delete=models.CASCADE,
        related_name='objetivos_especificos'
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion
    

# =========================================================
# ETAPAS
# =========================================================
class Etapa(models.Model):

    TIPOS_ETAPA = (

    ("INTRODUCTION", "Introducción"),

    ("THEORY", "Marco Teórico"),

    ("OBJECTIVES", "Objetivos"),

    ("CONCEPTS", "Conceptos Básicos"),

    ("FORMULAS", "Fórmulas"),

    ("PRACTICE", "Práctica"),

    ("SIMULATION_AR", "Simulación AR"),

    ("COMPARISON", "Comparación"),

    ("REPORT", "Informe"),

    ("SUBMIT", "Envío"),

)

    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.CASCADE,
        related_name='etapas'
    )

    nombre = models.CharField(
        max_length=100
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS_ETAPA
    )

    orden = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('laboratorio', 'tipo')
        ordering = ['orden']

    def __str__(self):
        return f"{self.orden}. {self.nombre}"


# =========================================================
# GRUPO ACADEMICO
# =========================================================
class GrupoAcademico(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grupos'
    )

    grado = models.CharField(
        max_length=20
    )

    jornada = models.CharField(
        max_length=20
    )

    activo = models.BooleanField(
        default=True
    )

    codigo_ingreso = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )

    def generar_codigo_ingreso(self):

        while True:

            codigo = uuid.uuid4().hex[:8].upper()

            existe = GrupoAcademico.objects.filter(
                codigo_ingreso=codigo
            ).exists()

            if not existe:
                return codigo


    class Meta:
        unique_together = ('nombre', 'profesor')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):

        if not self.codigo_ingreso:
            self.codigo_ingreso = self.generar_codigo_ingreso()

        super().save(*args, **kwargs)


# =========================================================
# ASIGNACION
# =========================================================
class Asignacion(models.Model):

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    codigo_ingreso = models.CharField(
            max_length=8,
            unique=True
        )

    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )

    grupo = models.ForeignKey(
        GrupoAcademico,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )

    fecha_inicio = models.DateTimeField()

    fecha_fin = models.DateTimeField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVO'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-fecha_creacion']
        unique_together = ('laboratorio', 'grupo')

    def clean(self):

        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError(
                "La fecha fin debe ser mayor que la fecha inicio."
            )
        
        if self.grupo.profesor != self.laboratorio.profesor:
            raise ValidationError(
                "El grupo y el laboratorio deben pertenecer al mismo profesor."
            )
        
    def save(self, *args, **kwargs):

        import uuid

        if not self.codigo_ingreso:

            while True:

                codigo = uuid.uuid4().hex[:8].upper()

                if not Asignacion.objects.filter(
                    codigo_ingreso=codigo
                ).exists():

                    self.codigo_ingreso = codigo
                    break

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grupo.nombre} - {self.laboratorio.titulo}"



# =========================================================
# SIMULACIÓN AR
# Configuración genérica para Unity / Android
# =========================================================

class SimulacionAR(models.Model):

    laboratorio = models.OneToOneField(
        "laboratorios.Laboratorio",
        on_delete=models.CASCADE,
        related_name="simulacion_ar_config"
    )

    lab_key = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True
    )

    unity_scene_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    display_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    version = models.CharField(
        max_length=50,
        blank=True,
        default="1.0.0"
    )

    enabled = models.BooleanField(
        default=True
    )

    intro_title = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    intro_text = models.TextField(
        blank=True,
        default=""
    )

    instructions = models.JSONField(
        default=list,
        blank=True
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=1
    )

    allow_resume = models.BooleanField(
        default=True
    )

    requires_camera = models.BooleanField(
        default=True
    )

    formulas = models.JSONField(
        default=list,
        blank=True
    )

    parameters = models.JSONField(
        default=dict,
        blank=True
    )

    options = models.JSONField(
        default=dict,
        blank=True
    )

    result_schema = models.JSONField(
        default=dict,
        blank=True
    )

    evaluation_context = models.TextField(
        blank=True,
        default=""
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "lab_key",
            "display_name"
        ]

    def __str__(self):
        nombre = self.display_name or self.lab_key or "Simulación AR"
        return f"{nombre} - Lab {self.laboratorio_id}"

# =========================================================
# PREGUNTAS DEL LABORATORIO
# Preguntas genéricas para móvil / evaluación
# =========================================================

class PreguntaLaboratorio(models.Model):

    TIPOS = (
        ("SABER", "Saber"),
        ("SABER_HACER", "Saber hacer"),
        ("ANALISIS", "Análisis"),
        ("REFLEXION", "Reflexión"),
        ("CIERRE", "Cierre"),
    )

    INPUT_TYPES = (
        ("TEXT", "Texto"),
        ("TEXTAREA", "Texto largo"),
        ("NUMBER", "Número"),
        ("BOOLEAN", "Booleano"),
        ("SELECT", "Selección"),
        ("MULTI_SELECT", "Selección múltiple"),
    )

    laboratorio = models.ForeignKey(
        "laboratorios.Laboratorio",
        on_delete=models.CASCADE,
        related_name="preguntas"
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS,
        default="ANALISIS"
    )

    key = models.CharField(
        max_length=100
    )

    titulo = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    enunciado = models.TextField(
        blank=True,
        default=""
    )

    input_type = models.CharField(
        max_length=30,
        choices=INPUT_TYPES,
        default="TEXTAREA"
    )

    required = models.BooleanField(
        default=True
    )

    order = models.PositiveSmallIntegerField(
        default=1
    )

    options = models.JSONField(
        default=list,
        blank=True
    )

    evaluation_hint = models.TextField(
        blank=True,
        default=""
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "id"]
        unique_together = (
            "laboratorio",
            "key"
        )

    def __str__(self):
        return f"{self.laboratorio_id} - {self.key}"
    
    