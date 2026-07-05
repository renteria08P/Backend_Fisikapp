from rest_framework import serializers
from .models import (
    ConceptoLaboratorio,
    ConceptosBasicos,
    Practica,
    Procedimiento,
    Formula,
    Recursos,
)


class RecursosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recursos
        fields = '__all__'

class ConceptosBasicosSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ConceptosBasicos
        fields = '__all__'

class ConceptoLaboratorioSerializer(serializers.ModelSerializer):

    concepto = ConceptosBasicosSerializer(
        read_only=True
    )

    concepto_id = serializers.PrimaryKeyRelatedField(
        queryset=ConceptosBasicos.objects.all(),
        source="concepto",
        write_only=True
    )
    

    recursos = RecursosSerializer(
        many=True,
        read_only=True
    )

    recursos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Recursos.objects.all(),
        many=True,
        write_only=True,
        source="recursos",
        required=False
    )

    def create(self, validated_data):

        recursos = validated_data.pop(
            "recursos",
            []
        )

        concepto_laboratorio = ConceptoLaboratorio.objects.create(
            **validated_data
        )

        concepto_laboratorio.recursos.set(recursos)

        return concepto_laboratorio
    
    def update(self, instance, validated_data):

        recursos = validated_data.pop(
            "recursos",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if recursos is not None:
            instance.recursos.set(recursos)

        return instance

    class Meta:
        model = ConceptoLaboratorio
        fields = [
            "id",
            "laboratorio",
            "concepto",
            "concepto_id",
            "recursos",
            "recursos_ids"
        ]

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = '__all__'

class ProcedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimiento
        fields = '__all__'

class FormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formula
        fields = '__all__'

