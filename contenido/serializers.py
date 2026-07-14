from rest_framework import serializers
import os
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
        fields = "__all__"

    def validate_archivo(self, value):

        if not value:
            return value

        extension = os.path.splitext(value.name)[1].lower()

        extensiones_permitidas = [
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".zip",
        ]

        if extension not in extensiones_permitidas:
            raise serializers.ValidationError(
                "Solo se permiten archivos PDF, Word, Excel, PowerPoint o ZIP."
            )

        return value

class ConceptosBasicosSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConceptosBasicos
        fields = "__all__"


class ConceptoLaboratorioSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        required=False
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

    concepto_original = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = ConceptoLaboratorio
        fields = [
            "id",
            "laboratorio",

            "concepto_original",

            "concepto",
            "descripcion",
            "ejemplo",
            "tipo",

            "recursos",
            "recursos_ids",
        ]

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

        validated_data.pop(
            "concepto_original",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if recursos is not None:
            instance.recursos.set(recursos)

        return instance


class PracticaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Practica
        fields = "__all__"


class ProcedimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Procedimiento
        fields = "__all__"


class FormulaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formula
        fields = "__all__"

    

class ProcedimientoSwaggerSerializer(serializers.Serializer):

    laboratorio = serializers.IntegerField()

    paso_numero = serializers.IntegerField()

    descripcion = serializers.CharField()

    orden = serializers.IntegerField()

    imagen = serializers.ImageField(
        required=False
    )