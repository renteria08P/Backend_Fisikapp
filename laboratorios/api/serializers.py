from rest_framework import serializers
from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo,
    LaboratorioProfesor
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

# ======================================
# LABORATORIO BASE
# ======================================
class LaboratorioSerializer(serializers.ModelSerializer):
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    codigo_lab = serializers.CharField(read_only=True)

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

    profesor_nombre = serializers.CharField(source='profesor.nombre', read_only=True)

    class Meta:
        model = LaboratorioProfesor
        fields = '__all__'
        read_only_fields = [
            'codigo_lab'
        ]

    profesor = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    codigo_lab = serializers.CharField(
        read_only=True
    )

    # MOSTRAR DATOS DEL LABORATORIO BASE
    titulo_lab = serializers.CharField(
        source='laboratorio.titulo_lab',
        read_only=True
    )

    categoria = serializers.CharField(
        source='laboratorio.categoria.nombre',
        read_only=True
    )

    resumen = serializers.CharField(required=False)
    prologo = serializers.CharField(required=False)
    introduccion = serializers.CharField(required=False)
    marco_teorico = serializers.CharField(required=False)

# =========================================================
# ADMIN - LABORATORIO
# =========================================================
class LaboratorioProfesorAdminSerializer(serializers.ModelSerializer):

    titulo = serializers.CharField(source="laboratorio.titulo_lab", read_only=True)

    categoria = serializers.CharField(source="laboratorio.categoria.nombre", read_only=True)

    creador = serializers.CharField(source="profesor.nombre", read_only=True)

    estado = serializers.BooleanField(read_only=True)

    ultimo_ingreso = serializers.DateTimeField(source="fecha_actualizacion", read_only=True)

    class Meta:
        model = LaboratorioProfesor
        fields = [
            "titulo",
            "categoria",
            "creador",
            "estado",
            "ultimo_ingreso"
        ]