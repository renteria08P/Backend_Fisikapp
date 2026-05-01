from rest_framework import serializers
from .models import Informe, Resultado, Conclusiones, Recomendaciones


class ConclusionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conclusiones
        fields = '__all__'


class RecomendacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendaciones
        fields = '__all__'


class InformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informe
        fields = [
            'id',
            'laboratorio',
            'desarrollo',
            'analisis',
            'autor',
            'fecha'
        ]

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'

