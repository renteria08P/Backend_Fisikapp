from rest_framework import serializers

from laboratorios.models import Laboratorio
from .models import Inscripcion
from .models import GrupoEstudiante


class InscripcionSerializer(serializers.ModelSerializer):

    laboratorio_titulo = serializers.CharField(
        source='asignacion.laboratorio.titulo',
        read_only=True
    )

    class Meta:
        model = Inscripcion

        fields = [
            "id",
            "laboratorio_titulo",
            "asignacion",
            "fecha_inscripcion"
        ]

        read_only_fields = (
            "id",
            "fecha_inscripcion"
        )
# =========================================================
# GRUPO ACADEMICO
# =========================================================
class GrupoLaboratorioSerializer(
    serializers.ModelSerializer
):

    asignacion_id = serializers.IntegerField(
        source='asignacion.id',
        read_only=True
    )

    titulo = serializers.CharField(
        source='asignacion.laboratorio.titulo',
        read_only=True
    )

    categoria = serializers.CharField(
        source='asignacion.laboratorio.plantilla.categoria.nombre',
        read_only=True
    )

    profesor = serializers.CharField(
        source='asignacion.laboratorio.profesor.nombre',
        read_only=True
    )

    fecha_asignado = serializers.DateTimeField(
        source='fecha_inscripcion',
        read_only=True
    )

    fecha_limite = serializers.DateTimeField(
        source='asignacion.fecha_fin',
        read_only=True
    )

    fecha_entrega = serializers.SerializerMethodField()

    estado = serializers.SerializerMethodField()

    nota = serializers.SerializerMethodField()


    def get_estado(self, obj):

        if hasattr(obj, "entrega"):
            return obj.entrega.estado

        return "BORRADOR"
    

    def get_fecha_entrega(self, obj):

        if hasattr(obj, "entrega"):
            return obj.entrega.fecha_entrega

        return None
    
    def get_nota(self, obj):

        if not hasattr(obj, "entrega"):
            return None

        evaluacion = getattr(
            obj.entrega,
            "evaluacion_docente",
            None
        )

        if evaluacion:
            return evaluacion.calificacion

        return None
    
    class Meta:

        model = Inscripcion

        fields = [
            "id",
            "asignacion_id",
            "titulo",
            "categoria",
            "profesor",
            "estado",
            "nota",
            "fecha_asignado",
            "fecha_entrega",
            "fecha_limite"
    ]
        

# =========================================================
# GRUPO ESTUDIANTE
# =========================================================
class GrupoEstudianteSerializer(serializers.ModelSerializer):

    grupo_nombre = serializers.CharField(
        source="grupo.nombre",
        read_only=True
    )

    codigo_ingreso = serializers.CharField(
        source="grupo.codigo_ingreso",
        read_only=True
    )

    class Meta:
        model = GrupoEstudiante
        fields = [
            "id",
            "grupo",
            "grupo_nombre",
            "codigo_ingreso",
            "estado",
            "fecha_inscripcion",
        ]

        read_only_fields = [
            "id",
            "fecha_inscripcion",
        ]
