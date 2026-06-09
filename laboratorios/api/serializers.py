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
# OBJETIVOS ESPECIFICOS
# =========================================================
class ObjetivoEspecificoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoEspecifico
        fields = '__all__'


# =========================================================
# OBJETIVO GENERAL
# =========================================================
class ObjetivoGeneralSerializer(serializers.ModelSerializer):

    objetivos_especificos = ObjetivoEspecificoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ObjetivoGeneral
        fields = '__all__'


from laboratorios.models import GrupoAcademico

class GrupoAcademicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoAcademico
        fields = "__all__"
        read_only_fields = ["profesor"]


from laboratorios.models import Asignacion

class AsignacionSerializer(serializers.ModelSerializer):

    laboratorio_titulo = serializers.CharField(
        source="laboratorio.titulo",
        read_only=True
    )

    grupo_nombre = serializers.CharField(
        source="grupo.nombre",
        read_only=True
    )

    class Meta:
        model = Asignacion
        fields = "__all__"
        read_only_fields = [
            "profesor",
            "fecha_creacion"
        ]

from laboratorios.models import PlantillaLaboratorio

class PlantillaLaboratorioSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PlantillaLaboratorio
        fields = "__all__"

# =========================================================
# LABORATORIO
# =========================================================
class LaboratorioSerializer(serializers.ModelSerializer):

    titulo_lab = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    categoria_nombre = serializers.CharField(
        source='plantilla.categoria.nombre',
        read_only=True
    )

    profesor_nombre = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    creador = serializers.IntegerField(
        source='profesor.id',
        read_only=True
    )

    codigo_lab = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Laboratorio
        fields = '__all__'


# =========================================================
# LABORATORIO PROFESOR
# =========================================================
class LaboratorioProfesorSerializer(serializers.ModelSerializer):

    titulo_lab = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    profesor_nombre = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    categoria = serializers.CharField(
        source='plantilla.categoria.nombre',
        read_only=True
    )

    class Meta:
        model = Laboratorio
        fields = '__all__'

        read_only_fields = [
            'codigo_lab',
            'profesor',
            'fecha_creacion',
            'fecha_actualizacion'
        ]


# =========================================================
# ADMIN - LABORATORIOS PROFESOR
# =========================================================
class LaboratorioProfesorAdminSerializer(
    serializers.ModelSerializer
):

    titulo = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    categoria = serializers.CharField(
        source='plantilla.categoria.nombre',
        read_only=True
    )

    creador = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    ultimo_ingreso = serializers.DateTimeField(
        source='fecha_actualizacion',
        read_only=True
    )

    class Meta:
        model = Laboratorio

        fields = [
            'id',
            'titulo',
            'categoria',
            'creador',
            'estado',
            'ultimo_ingreso'
        ]