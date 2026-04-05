from rest_framework import serializers
from .models import Inscripcion
from .models import ConceptosBasicos, Practicas, Procedimientos

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'
        read_only_fields = ('id',)

class ConceptosBasicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptosBasicos
        fields = '__all__'


class PracticasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practicas
        fields = '__all__'


class ProcedimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimientos
        fields = '__all__'