from rest_framework import serializers

from laboratorios.models import Asignacion

from laboratorios.models import (
    Laboratorio,
    Categoria,
    ObjetivoGeneral,
    ObjetivoEspecifico,
    PlantillaObjetivoGeneral,
    PlantillaObjetivoEspecifico
)

from contenido.serializers import (
    ConceptosBasicosSerializer,
    FormulaSerializer,
    ProcedimientoSerializer,
    PracticaSerializer,
)

from contenido.models import (
    Practica,
    Procedimiento,
    Formula,
)

# =========================================================
# CATEGORIA
# =========================================================
class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
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


# =========================================================
# OBJETIVOS PLANTILLA
# =========================================================

class PlantillaObjetivoEspecificoSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PlantillaObjetivoEspecifico
        fields = "__all__"


class PlantillaObjetivoGeneralSerializer(
    serializers.ModelSerializer
):

    objetivos_especificos = (
        PlantillaObjetivoEspecificoSerializer(
            many=True,
            read_only=True
        )
    )

    class Meta:
        model = PlantillaObjetivoGeneral
        fields = "__all__"


#=====================================================
# GRUPO ACADEMICO
# =========================================================
from laboratorios.models import GrupoAcademico

class GrupoAcademicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoAcademico
        fields = "__all__"
        read_only_fields = ["profesor"]


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
            "fecha_creacion",
            "codigo_ingreso"   
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

    codigo_ingreso = serializers.CharField(
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

    objetivo_general = ObjetivoGeneralSerializer(
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

    plantilla_titulo = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    plantilla_categoria = serializers.CharField(
        source='plantilla.categoria.nombre',
        read_only=True
    )

    def create(self, validated_data):

        laboratorio = Laboratorio.objects.create(
            **validated_data
        )

        plantilla = laboratorio.plantilla

        try:

            objetivo_plantilla = (
                plantilla.objetivo_general
            )

            objetivo_general = (
                ObjetivoGeneral.objects.create(
                    laboratorio=laboratorio,
                    descripcion=objetivo_plantilla.descripcion
                )
            )

            for objetivo in (
                objetivo_plantilla
                .objetivos_especificos
                .all()
            ):

                ObjetivoEspecifico.objects.create(
                    objetivo_general=objetivo_general,
                    descripcion=objetivo.descripcion
                )

        except PlantillaObjetivoGeneral.DoesNotExist:
            pass

        laboratorio.conceptos_basicos.set(
            plantilla.conceptos_basicos.all()
        )


        for practica in plantilla.practicas.all():

            nueva = Practica.objects.create(
                laboratorio=laboratorio,
                nombre_practica=practica.nombre_practica,
                objetivo=practica.objetivo,
                descripcion=practica.descripcion,
                materiales=practica.materiales,
                calculos=practica.calculos
            )

            nueva.conceptos.set(
                practica.conceptos.all()
            )

        for procedimiento in plantilla.procedimientos.all():

            Procedimiento.objects.create(
                laboratorio=laboratorio,
                muestras=procedimiento.muestras,
                calculos=procedimiento.calculos,
                resultados=procedimiento.resultados
            )

        for formula in plantilla.formulas.all():

            Formula.objects.create(
                laboratorio=laboratorio,
                nombre=formula.nombre,
                descripcion=formula.descripcion,
                expresion=formula.expresion
            )

        return laboratorio

    class Meta:
        model = Laboratorio
        fields = '__all__'

        read_only_fields = [
            'codigo_ingreso',
            'profesor',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
# =========================================================
# Gestión de Laboratorios - Admin
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

# =========================================================
# LABORATORIO ESTUDIANTE LISTA
# =========================================================
class LaboratorioEstudianteListSerializer(
    serializers.ModelSerializer
):

    titulo = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    profesor = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    class Meta:
        model = Laboratorio

        fields = [
            'id',
            'titulo',
            'profesor',
            'estado'
        ]

# =========================================================
# LABORATORIO ESTUDIANTE
# =========================================================
class LaboratorioEstudianteSerializer(
    serializers.ModelSerializer
):
    
    objetivo_general = ObjetivoGeneralSerializer(
        read_only=True
    )

    titulo_lab = serializers.CharField(
        source='plantilla.titulo',
        read_only=True
    )

    categoria = serializers.CharField(
        source='plantilla.categoria.nombre',
        read_only=True
    )

    profesor_nombre = serializers.CharField(
        source='profesor.nombre',
        read_only=True
    )

    conceptos_basicos = ConceptosBasicosSerializer(
        many=True,
        read_only=True
    )

    formulas = FormulaSerializer(
        many=True,
        read_only=True
    )

    procedimientos = ProcedimientoSerializer(
        many=True,
        read_only=True
    )

    practicas = PracticaSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Laboratorio

        fields = [
            "id",

            "titulo_lab",
            "categoria",
            "profesor_nombre",

            "resumen",
            "prologo",
            "introduccion",
            "marco_teorico",

            "objetivo_general",
            "conceptos_basicos",
            "formulas",
            "procedimientos",
            "practicas",

            "estado",
            "fecha_creacion"
        ]
    
