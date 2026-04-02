from rest_framework import serializers
from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo
)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = '__all__'


class PalabraClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalabraClave
        fields = '__all__'


class LaboratorioSerializer(serializers.ModelSerializer):
    creador = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Laboratorio
        fields = '__all__'

    def validate_codigo_lab(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "El código debe tener al menos 5 caracteres"
            )
        return value