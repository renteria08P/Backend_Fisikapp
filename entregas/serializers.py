from rest_framework import serializers
from .models import Pregunta, ResultadoSimulacion
from .models import Respuesta
from .models import Entrega
from .models import ResultadoPractica


class PreguntaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pregunta
        fields = '__all__'


class RespuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Respuesta
        fields = '__all__'


class EntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrega
        fields = '__all__'


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