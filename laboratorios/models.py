from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


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


# =========================================================
# PLANTILLA DE LABORATORIO (ADMIN)
# =========================================================
class PlantillaLaboratorio(models.Model):

    resumen = models.TextField()

    introduccion = models.TextField()

    marco_teorico = models.TextField()

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
        unique=True
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

    simulacion = models.BooleanField(
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

    def __str__(self):
        return self.titulo
    

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

    conceptos_basicos = models.ManyToManyField(
        'contenido.ConceptosBasicos',
        blank=True,
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

        constraints = [
            models.UniqueConstraint(
                fields=['plantilla', 'profesor'],
                name='unique_plantilla_profesor'
            )
        ]

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
        ('CONCEPTOS', 'Conceptos Básicos'),
        ('PRACTICA', 'Práctica'),
        ('INFORME', 'Informe'),
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
        max_length=20,
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

    class Meta:
        unique_together = ('nombre', 'profesor')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


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

    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='asignaciones_creadas'
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

        if self.profesor != self.grupo.profesor:
            raise ValidationError(
                "El grupo no pertenece al profesor."
            )

        if self.profesor != self.laboratorio.profesor:
            raise ValidationError(
                "El laboratorio no pertenece al profesor."
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


