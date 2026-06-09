from rest_framework import serializers
from .models import Inscripcion


class InscripcionSerializer(serializers.ModelSerializer):

    estudiante_nombre = serializers.CharField(
        source='estudiante.nombre',
        read_only=True
    )

    laboratorio_titulo = serializers.CharField(
        source='asignacion.laboratorio.titulo',
        read_only=True
    )

    class Meta:
        model = Inscripcion

        fields = '__all__'

        read_only_fields = (
            'id',
            'fecha_inscripcion'
        )