from rest_framework import serializers
from .models import ResultadoSimulacion

from .models import Entrega
from .models import ResultadoPractica


class EntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrega
        fields = "__all__"

        read_only_fields = [
            "estado",
            "fecha_inicio",
            "fecha_entrega",
            "fecha_creacion",
            "fecha_actualizacion"
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