from rest_framework import serializers
from .models import ResultadoSimulacion

from .models import (
    Entrega,
    ResultadoPractica,
    EntregaLaboratorioUnificada,
)


class EntregaLaboratorioUnificadaSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntregaLaboratorioUnificada
        fields = [
            "id",
            "practice",
            "simulation",
            "comparison",
            "questions",
            "report",
            "device",
            "llm_payload",
            "raw_payload",
            "fecha_creacion",
            "fecha_actualizacion",
        ]


class EntregaSerializer(serializers.ModelSerializer):

    entrega_unificada = EntregaLaboratorioUnificadaSerializer(
        read_only=True
    )

    estudiante_nombre = serializers.CharField(
        source="inscripcion.estudiante.nombre",
        read_only=True
    )

    estudiante_correo = serializers.CharField(
        source="inscripcion.estudiante.correo",
        read_only=True
    )

    laboratorio_titulo = serializers.CharField(
        source="inscripcion.asignacion.laboratorio.titulo",
        read_only=True
    )

    grupo_nombre = serializers.CharField(
        source="inscripcion.asignacion.grupo.nombre",
        read_only=True
    )

    class Meta:
        model = Entrega

        fields = [
            "id",
            "tipo_reporte",
            "estado",
            "fecha_inicio",
            "fecha_entrega",
            "observaciones",
            "fecha_creacion",
            "fecha_actualizacion",
            "inscripcion",

            "estudiante_nombre",
            "estudiante_correo",
            "laboratorio_titulo",
            "grupo_nombre",

            "entrega_unificada",
        ]

class ResultadoPracticaSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ResultadoPractica
        fields = '__all__'



class ResultadoSimulacionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ResultadoSimulacion
        fields = '__all__'