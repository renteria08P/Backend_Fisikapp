from rest_framework import serializers
from .models import Informe, Resultado, Conclusiones, Recomendaciones


class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'


class ConclusionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conclusiones
        fields = '__all__'


class RecomendacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendaciones
        fields = '__all__'


class InformeSerializer(serializers.ModelSerializer):
    resultados = ResultadoSerializer(many=True, read_only=True)
    conclusiones = ConclusionesSerializer(many=True, read_only=True)
    recomendaciones = RecomendacionesSerializer(many=True, read_only=True)

    class Meta:
        model = Informe
        fields = '__all__'


class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'

