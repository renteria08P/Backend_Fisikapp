from rest_framework import serializers
from .models import (
    ConceptosBasicos,
    Practica,
    Procedimiento,
    Formula,
    Bibliografia,
    Recursos
)

from .models import (
    PlantillaPractica,
    PlantillaProcedimiento,
    PlantillaFormula,
    PlantillaBibliografia
)

class RecursosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recursos
        fields = '__all__'

    def validate(self, data):
        archivo = data.get('archivo', getattr(self.instance, 'archivo', None))
        url = data.get('url', getattr(self.instance, 'url', None))

        if not archivo and not url:
            raise serializers.ValidationError(
                "Debes subir un archivo o proporcionar una URL."
            )

        return data

    def validate_archivo(self, value):
        if value:
            ext = value.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise serializers.ValidationError(
                    "Solo se permiten archivos PDF, DOC o DOCX."
                )
        return value


class ConceptosBasicosSerializer(serializers.ModelSerializer):
    
    # Para leer (GET)
    recursos = RecursosSerializer(many=True, read_only=True)

    #  Para JSON (crear con URLs)
    recursos_data = RecursosSerializer(many=True, write_only=True, required=False)

    # Para form-data (usar IDs)
    recursos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Recursos.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='recursos'
    )

    class Meta:
        model = ConceptosBasicos
        fields = '__all__'

    def create(self, validated_data):
        recursos_data = validated_data.pop('recursos_data', [])
        recursos_ids = validated_data.pop('recursos', [])

        concepto = ConceptosBasicos.objects.create(**validated_data)

        # Caso 1: JSON (crear recursos nuevos)
        for recurso_data in recursos_data:
            recurso = Recursos.objects.create(**recurso_data)
            concepto.recursos.add(recurso)

        # Caso 2: form-data (usar recursos existentes)
        for recurso in recursos_ids:
            concepto.recursos.add(recurso)

        return concepto

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

class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = '__all__'

# =========================================================
# PLANTILLA PRACTICA
# =========================================================
class PlantillaPracticaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlantillaPractica
        fields = "__all__"


# =========================================================
# PLANTILLA PROCEDIMIENTO
# =========================================================
class PlantillaProcedimientoSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PlantillaProcedimiento
        fields = "__all__"


# =========================================================
# PLANTILLA FORMULA
# =========================================================
class PlantillaFormulaSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PlantillaFormula
        fields = "__all__"


# =========================================================
# PLANTILLA BIBLIOGRAFIA
# =========================================================
class PlantillaBibliografiaSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PlantillaBibliografia
        fields = "__all__"