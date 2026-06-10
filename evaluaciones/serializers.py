from rest_framework import serializers

from .models import (
    EvaluacionProfesor,
    EvaluacionIA
)

class EvaluacionProfesorSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = EvaluacionProfesor
        fields = '__all__'
        read_only_fields = [
            'profesor',
            'fecha_evaluacion'
        ]


class EvaluacionIASerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = EvaluacionIA
        fields = '__all__'