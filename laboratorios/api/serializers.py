from rest_framework import serializers
from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    ObjetivoGeneral,
    ObjetivoEspecifico
)

# =========================================================
# CATEGORIA
# =========================================================
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


# =========================================================
# PALABRAS CLAVE
# =========================================================
class PalabraClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalabraClave
        fields = '__all__'


# =========================================================
# OBJETIVOS
# =========================================================
class ObjetivoEspecificoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoEspecifico
        fields = '__all__'


class ObjetivoGeneralSerializer(serializers.ModelSerializer):

    objetivos_especificos = ObjetivoEspecificoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ObjetivoGeneral
        fields = '__all__'

# =========================================================
# LABORATORIO BASE
# =========================================================
class LaboratorioSerializer(serializers.ModelSerializer):

    creador = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    codigo_lab = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Laboratorio
        fields = '__all__'

    def validate_codigo_lab(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "El código debe tener al menos 5 caracteres"
            )
        return value


# =========================================================
# LABORATORIO PROFESOR
# =========================================================
class LaboratorioProfesorSerializer(serializers.ModelSerializer):

    id_padre = serializers.PrimaryKeyRelatedField(
        queryset=Laboratorio.objects.all()
    )

    profesor_nombre = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    class Meta:
        model = Laboratorio
        fields = '__all__'

        read_only_fields = [
            'codigo_lab',
            'profesor',
            'titulo_lab',
            'categoria',
            'palabras_clave',
            'creador',
            'resumen',
            'prologo',
            'introduccion',
            'marco_teorico',
            'fecha_creacion',
            'conceptos_basicos',
            'fecha_actualizacion'
        ]


# =========================================================
# ADMIN - LABORATORIOS PROFESOR
# =========================================================
class LaboratorioProfesorAdminSerializer(serializers.ModelSerializer):

    titulo = serializers.CharField(
        source="titulo_lab",
        read_only=True
    )

    categoria = serializers.CharField(
        source="categoria.nombre",
        read_only=True
    )

    creador = serializers.CharField(
        source="profesor.nombre",
        read_only=True
    )

    estado = serializers.BooleanField(
        read_only=True
    )

    ultimo_ingreso = serializers.DateTimeField(
        source="fecha_actualizacion",
        read_only=True
    )

    class Meta:
        model = Laboratorio

        fields = [
            "titulo",
            "categoria",
            "creador",
            "estado",
            "ultimo_ingreso"
        ]

