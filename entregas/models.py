from django.db import models


# =========================================================
# ENTREGAS
# =========================================================

class Entrega(models.Model):

    ESTADOS = (
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('GENERADO', 'Generado'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    )

    TIPOS = (
        ('PRACTICA', 'Práctica'),
        ('SIMULACION', 'Simulación'),
        ('INTEGRADA', 'Entrega integrada'),
    )

    inscripcion = models.OneToOneField(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='entrega'
    )

    tipo_reporte = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='PRACTICA'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='BORRADOR'
    )

    fecha_inicio = models.DateTimeField(
        auto_now_add=True
    )

    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-fecha_creacion']

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.inscripcion.estudiante} - "
            f"{self.inscripcion.asignacion.laboratorio.titulo}"
        )

# =========================================================
# RESULTADO PRÁCTICA
# =========================================================

class ResultadoPractica(models.Model):

    entrega = models.OneToOneField(
        Entrega,
        on_delete=models.CASCADE,
        related_name='resultado_practica'
    )

    observaciones = models.TextField()

    datos_obtenidos = models.JSONField()

    conclusiones = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Resultado práctica {self.entrega.id}"

# =========================================================
# RESULTADO SIMULACIÓN
# =========================================================

class ResultadoSimulacion(models.Model):

    STATUS = (
        ("completed", "Completado"),
        ("abandoned", "Abandonado"),
        ("in_progress", "En progreso"),
    )

    EXIT_REASONS = (
        ("completed", "Completado"),
        ("max_attempts", "Máximo de intentos"),
        ("user_exit", "Salida del usuario"),
    )

    entrega = models.OneToOneField(
        Entrega,
        on_delete=models.CASCADE,
        related_name='resultado_simulacion'
    )

    run_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        default=""
    )

    completed = models.BooleanField(
        default=False
    )

    result_status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="in_progress"
    )

    exit_reason = models.CharField(
        max_length=30,
        choices=EXIT_REASONS,
        default="completed"
    )

    best_attempt = models.PositiveSmallIntegerField(
        default=0
    )

    best_distance = models.FloatField(
        default=0
    )

    average_distance = models.FloatField(
        default=0
    )

    successful_attempts = models.PositiveSmallIntegerField(
        default=0
    )

    failed_attempts = models.PositiveSmallIntegerField(
        default=0
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    raw_result = models.JSONField(
        null=True,
        blank=True
    )

    platform = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    ar_provider = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    unity_version = models.CharField(
        max_length=30,
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
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Resultado simulación {self.entrega.id}"

# =========================================================
# INTENTO SIMULACIÓN
# =========================================================

class IntentoSimulacion(models.Model):

    IMPACT_TYPES = (
        ("HitTarget", "Hit Target"),
        ("MissedTarget", "Missed Target"),
    )

    resultado = models.ForeignKey(
        ResultadoSimulacion,
        on_delete=models.CASCADE,
        related_name="intentos"
    )

    numero = models.PositiveSmallIntegerField()

    hit = models.BooleanField(
        default=False
    )

    power = models.FloatField()

    angle = models.FloatField()

    impact_distance = models.FloatField()

    impact_horizontal_distance = models.FloatField()

    impact_distance_to_target = models.FloatField()

    impact_height = models.FloatField()

    impact_type = models.CharField(
        max_length=30,
        choices=IMPACT_TYPES
    )

    impact_x = models.FloatField()

    impact_y = models.FloatField()

    impact_z = models.FloatField()

    target_x = models.FloatField()

    target_y = models.FloatField()

    target_z = models.FloatField()

    created_at = models.DateTimeField()

    class Meta:
        ordering = ["numero"]

        unique_together = (
            ("resultado", "numero"),
        )

    def __str__(self):
        return f"Intento {self.numero}"
    
# =========================================================
# ENTREGA LABORATORIO UNIFICADA
# Nuevo contrato móvil.
# No reemplaza los modelos legacy de práctica/simulación.
# =========================================================

class EntregaLaboratorioUnificada(models.Model):

    entrega = models.OneToOneField(
        Entrega,
        on_delete=models.CASCADE,
        related_name="entrega_unificada"
    )

    practice = models.JSONField(
        default=dict,
        blank=True
    )

    simulation = models.JSONField(
        default=dict,
        blank=True
    )

    comparison = models.JSONField(
        default=dict,
        blank=True
    )

    questions = models.JSONField(
        default=list,
        blank=True
    )

    report = models.JSONField(
        default=dict,
        blank=True
    )

    device = models.JSONField(
        default=dict,
        blank=True
    )

    llm_payload = models.JSONField(
        default=dict,
        blank=True
    )

    raw_payload = models.JSONField(
        default=dict,
        blank=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Entrega unificada {self.entrega_id}"