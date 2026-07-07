from rest_framework import serializers
from laboratorios.models import PlantillaLaboratorio
from cloudinary.utils import cloudinary_url
from contenido.models import ConceptoLaboratorio
from laboratorios.models import Asignacion
from django.db import transaction
from rest_framework import serializers

from laboratorios.models import (
    Laboratorio,
    Categoria,
    ObjetivoGeneral,
    ObjetivoEspecifico,
    PlantillaObjetivoGeneral,
    PlantillaObjetivoEspecifico,
)

from contenido.serializers import (
    ConceptoLaboratorioSerializer,
    FormulaSerializer,
    ProcedimientoSerializer,
    PracticaSerializer,
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

    id = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = ObjetivoEspecifico
        fields = "__all__"

# =========================================================
# OBJETIVO GENERAL
# =========================================================
class ObjetivoGeneralSerializer(serializers.ModelSerializer):

    objetivos_especificos = ObjetivoEspecificoSerializer(
        many=True,
        required=False
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
            "fecha_creacion",
            "codigo_ingreso"   
        ]

class PlantillaLaboratorioSerializer(
    serializers.ModelSerializer
):


    creador_nombre = serializers.CharField(
        source='creado_por.nombre',
        read_only=True
    )

    imagen_portada = serializers.ImageField(
        write_only=True,
        required=False,
        allow_null=True
    )

    imagen_portada_url = serializers.SerializerMethodField()

    def get_imagen_portada_url(self, obj):

        if not obj.imagen_portada:
            return None

        url, _ = cloudinary_url(
            str(obj.imagen_portada),
            secure=True
        )

        return url

    categoria_nombre = serializers.CharField(
        source="categoria.nombre",
        read_only=True
    )

    objetivo_general = PlantillaObjetivoGeneralSerializer(
        read_only=True
    )

    class Meta:
        model = PlantillaLaboratorio

        fields = [
            "id",
            "titulo",
            "descripcion",
            "resumen",
            "introduccion",
            "marco_teorico",
            "imagen_portada",
            "imagen_portada_url",
            "lab_key",
            "estado",
            "fecha_creacion",
            "fecha_actualizacion",
            "categoria",
            "categoria_nombre",
            "creado_por",
            "creador_nombre",
            "conceptos_basicos",
            "objetivo_general",
        ]

        read_only_fields = [
            "creado_por",
            "fecha_creacion",
            "fecha_actualizacion",
        ]

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
        required=False
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

    imagen_portada = serializers.SerializerMethodField()

    def get_imagen_portada(self, obj):

        plantilla = getattr(obj, "plantilla", None)

        if plantilla and plantilla.imagen_portada:
            return plantilla.imagen_portada.url

        return None

    practicas = PracticaSerializer(
        many=True,
        read_only=True
    )

    procedimientos = ProcedimientoSerializer(
        many=True,
        read_only=True
    )

    formulas = FormulaSerializer(
        many=True,
        read_only=True
    )

    conceptos_basicos = ConceptoLaboratorioSerializer(
        source="conceptos_laboratorio",
        many=True,
        required=False,
        allow_null=True
    )

    def create(self, validated_data):

        plantilla = validated_data["plantilla"]

        laboratorio = Laboratorio.objects.create(
            resumen=plantilla.resumen,
            introduccion=plantilla.introduccion,
            marco_teorico=plantilla.marco_teorico,
            **validated_data
    )

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

        for concepto in plantilla.conceptos_basicos.all():

            ConceptoLaboratorio.objects.create(
                laboratorio=laboratorio,
                concepto_original=concepto,
                concepto=concepto.concepto,
                descripcion=concepto.descripcion,
                ejemplo=concepto.ejemplo,
                tipo=concepto.tipo
            )

        return laboratorio
    
    def update(self, instance, validated_data):

        objetivo_data = validated_data.pop(
            "objetivo_general",
            None
        )

        conceptos_data = validated_data.pop(
            "conceptos_laboratorio",
            None
        )

        # ==========================================
        # Actualizar datos del laboratorio
        # ==========================================
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # ==========================================
        # Actualizar objetivo general
        # ==========================================
        if objetivo_data is not None:

            objetivos_data = objetivo_data.pop(
                "objetivos_especificos",
                []
            )

            objetivo_general, _ = ObjetivoGeneral.objects.get_or_create(
                laboratorio=instance
            )

            if "descripcion" in objetivo_data:
                objetivo_general.descripcion = objetivo_data["descripcion"]

            objetivo_general.save()

            ids_recibidos = []

            for item in objetivos_data:

                objetivo_id = item.get("id")

                if objetivo_id:

                    objetivo = ObjetivoEspecifico.objects.filter(
                        id=objetivo_id,
                        objetivo_general=objetivo_general
                    ).first()

                    if not objetivo:
                        continue

                    objetivo.descripcion = item["descripcion"]
                    objetivo.save()

                    ids_recibidos.append(objetivo.id)

                else:

                    nuevo = ObjetivoEspecifico.objects.create(
                        objetivo_general=objetivo_general,
                        descripcion=item["descripcion"]
                    )

                    ids_recibidos.append(nuevo.id)

            if objetivos_data:
                ObjetivoEspecifico.objects.filter(
                    objetivo_general=objetivo_general
                ).exclude(
                    id__in=ids_recibidos
                ).delete()

        # ==========================================
        # Actualizar conceptos básicos
        # ==========================================
        if conceptos_data is not None:

            with transaction.atomic():

                for concepto_data in conceptos_data:
                    concepto_id = concepto_data.get("id")

                    if not concepto_id:
                        continue

                    concepto = ConceptoLaboratorio.objects.filter(
                        id=concepto_id,
                        laboratorio=instance
                    ).first()

                    if not concepto:
                        continue

                    recursos = concepto_data.pop("recursos", None)

                    print("RECURSOS PADRE:", recursos)
    

                    concepto_data.pop("laboratorio", None)
                    concepto_data.pop("concepto_original", None)

                    serializer = ConceptoLaboratorioSerializer(
                        instance=concepto,
                        data=concepto_data,
                        partial=True,
                        context=self.context
                    )

                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    if recursos is not None:
                        concepto.recursos.set(recursos)
                        print("RECURSOS GUARDADOS:", list(concepto.recursos.all()))

        return instance
            

    class Meta:
        model = Laboratorio
        fields = [
            "id",
            "titulo_lab",
            "objetivo_general",
            "profesor_nombre",
            "categoria",
            "plantilla_titulo",
            "plantilla_categoria",
            "imagen_portada",

            "resumen",
            "introduccion",
            "marco_teorico",

            "conceptos_basicos",
            "practicas",
            "procedimientos",
            "formulas",

            "estado",
            "generado_ia",
            "fecha_creacion",
            "fecha_actualizacion",

            "plantilla",
            "profesor",
        ]

        read_only_fields = [
            'profesor',
            "fecha_creacion",
        ]

        extra_kwargs = {
            "resumen": {"required": False},
            "introduccion": {"required": False},
            "marco_teorico": {"required": False},
        }


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

    imagen_portada = serializers.SerializerMethodField()
    def get_imagen_portada(self, obj):
        plantilla = getattr(obj, "plantilla", None)

        if plantilla and plantilla.imagen_portada:
            return plantilla.imagen_portada.url

        return None

    ultimo_ingreso = serializers.DateTimeField(
        source='fecha_actualizacion',
        read_only=True
    )

    generado_ia = serializers.BooleanField(
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
            'generado_ia',
            'imagen_portada',
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

    imagen_portada = serializers.SerializerMethodField()
    def get_imagen_portada(self, obj):
        plantilla = getattr(obj, "plantilla", None)

        if plantilla and plantilla.imagen_portada:
            return plantilla.imagen_portada.url

        return None

    class Meta:
        model = Laboratorio

        fields = [
            'id',
            'titulo',
            'profesor',
            'imagen_portada',
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

    conceptos_basicos = ConceptoLaboratorioSerializer(
        source="conceptos_laboratorio",
        many=True,
        read_only=True
    )

    imagen_portada = serializers.SerializerMethodField()
    def get_imagen_portada(self, obj):
        plantilla = getattr(obj, "plantilla", None)

        if plantilla and plantilla.imagen_portada:
            return plantilla.imagen_portada.url

        return None
    
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
            "imagen_portada",

            "resumen",
            "introduccion",
            "marco_teorico",

            "objetivo_general",
            "conceptos_basicos",
            "formulas",
            "procedimientos",
            "practicas",
            "fecha_creacion"
        ]


# =========================================================
# DASHBOARD ADMIN
# =========================================================

class DashboardAdminSerializer(serializers.Serializer):

    total_laboratorios = serializers.IntegerField()

    laboratorios_activos = serializers.IntegerField()

    laboratorios_inactivos = serializers.IntegerField()

    usuarios_admin = serializers.IntegerField()

    usuarios_profesor = serializers.IntegerField()

    usuarios_estudiante = serializers.IntegerField()

    laboratorios_ia = serializers.IntegerField()

    eficiencia_ia = serializers.IntegerField()

    ultimos_laboratorios = serializers.ListField()

    tendencia = serializers.DictField()



from rest_framework import serializers


class RecursosSwaggerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    url = serializers.CharField()

class ConceptoLaboratorioSwaggerSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    laboratorio = serializers.IntegerField(required=False)

    concepto = serializers.CharField()
    descripcion = serializers.CharField()
    ejemplo = serializers.CharField()
    tipo = serializers.CharField()

    recursos = RecursosSwaggerSerializer(
        many=True,
        required=False
    )

    # SOLO PARA DOCUMENTACIÓN
    recursos_ids = RecursosSwaggerSerializer(
        many=True,
        required=False
    )

class LaboratorioProfesorPatchSwaggerSerializer(serializers.Serializer):

    resumen = serializers.CharField(required=False)

    introduccion = serializers.CharField(required=False)

    marco_teorico = serializers.CharField(required=False)

    generado_ia = serializers.BooleanField(required=False)

    conceptos_basicos = ConceptoLaboratorioSwaggerSerializer(
        many=True,
        required=False
    )