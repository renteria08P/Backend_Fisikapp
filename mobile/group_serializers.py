from rest_framework import serializers
from inscripciones.models import GrupoEstudiante


class JoinGroupRequestSerializer(serializers.Serializer):
    codigo = serializers.CharField(
        max_length=20
    )
