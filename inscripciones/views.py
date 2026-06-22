from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inscripcion
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes  
from laboratorios.models import Asignacion
from evaluaciones.models import (
    EvaluacionProfesor
)


from .serializers import (
    InscripcionSerializer,
    GrupoLaboratorioSerializer
)
from rest_framework.generics import ListAPIView

from inscripciones.models import Inscripcion

class InscripcionesViewSet(viewsets.ModelViewSet):

    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = [
        'estudiante',
        'asignacion',
        'fecha_inscripcion'
    ]

    ordering_fields = [
        'fecha_inscripcion'
    ]

    @swagger_auto_schema(
        operation_summary="Listar inscripciones",
        operation_description="""
        Retorna todas las inscripciones registradas.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalle de inscripción",
        operation_description="""
        Retorna la información de una inscripción específica.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inscribir_usuario(request):

    codigo = request.data.get('codigo')

    if not codigo:
        return Response(
            {"error": "Debe enviar el código"},
            status=400
        )

    try:

        asignacion = Asignacion.objects.get(
            codigo_ingreso=codigo
        )

    except Asignacion.DoesNotExist:

        return Response(
            {"error": "Código inválido"},
            status=404
        )

    existe = Inscripcion.objects.filter(
        estudiante=request.user,
        asignacion=asignacion
    ).exists()

    if existe:

        return Response(
            {"error": "Ya estás inscrito"},
            status=400
        )

    inscripcion = Inscripcion.objects.create(
        estudiante=request.user,
        asignacion=asignacion
    )

    serializer = InscripcionSerializer(inscripcion)

    return Response(
        serializer.data,
        status=201
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_inscripciones(request):

    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user
    )

    serializer = InscripcionSerializer(
        inscripciones,
        many=True
    )

    return Response(serializer.data)

@swagger_auto_schema(method='put', request_body=InscripcionSerializer)
@api_view(['PUT', 'DELETE'])
def detalle_inscripcion(request, pk):
    try:
        inscripcion = Inscripcion.objects.get(pk=pk)
    except Inscripcion.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = InscripcionSerializer(inscripcion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        inscripcion.delete()
        return Response({"mensaje": "Eliminado correctamente"}, status=204)
    
# =============================================
#  MIS LABORATORIOS ESTUDIANTE
# =============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_laboratorios(request):

    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user
    )
    serializer = InscripcionSerializer(inscripciones, many=True)
    return Response(serializer.data)


# =============================================
#  MIS GRUPOS
# =============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_grupos(request):

    inscripciones = (
        Inscripcion.objects
        .filter(estudiante=request.user)
        .select_related(
            'asignacion__grupo',
            'asignacion__laboratorio__profesor',
            'entrega'
        )
    )

    grupos = {}

    for inscripcion in inscripciones:

        asignacion = inscripcion.asignacion
        grupo = asignacion.grupo

        if grupo.id not in grupos:

            grupos[grupo.id] = {
                "grupo_id": grupo.id,
                "grupo_nombre": grupo.nombre,

                "grado": grupo.grado,
                "jornada": grupo.jornada,

                "instructor_nombre": grupo.profesor.nombre,

                "total_laboratorios": 0,
                "laboratorios_activos": 0,

                "entregas_pendientes": 0,
                "entregas_enviadas": 0,
                "calificaciones_pendientes": 0,

                "actividades": []
            }

        estado_entrega = None

        grupos[grupo.id]["total_laboratorios"] += 1

        if asignacion.estado == "ACTIVO":
            grupos[grupo.id]["laboratorios_activos"] += 1

        if hasattr(inscripcion, 'entrega'):

            estado_entrega = inscripcion.entrega.estado

            if inscripcion.entrega.estado == "ENVIADA":
                grupos[grupo.id]["entregas_enviadas"] += 1

            if inscripcion.entrega.estado != "APROBADO":
                grupos[grupo.id]["entregas_pendientes"] += 1

            grupos[grupo.id]["calificaciones_pendientes"] += 1

        else:

            grupos[grupo.id]["entregas_pendientes"] += 1

        grupos[grupo.id]["actividades"].append({
            "laboratorio_id": asignacion.laboratorio.id,
            "laboratorio": asignacion.laboratorio.titulo,
            "estado_entrega": estado_entrega,
            "fecha_limite": asignacion.fecha_fin
        })

    return Response(
        list(grupos.values())
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grupo_laboratorios(request, grupo_id):

    inscripciones = (
        Inscripcion.objects
        .filter(
            estudiante=request.user,
            asignacion__grupo_id=grupo_id
        )
        .select_related(
            'asignacion',
            'asignacion__grupo',
            'asignacion__laboratorio',
            'asignacion__laboratorio__plantilla',
            'entrega',
            'entrega__evaluacion_docente'
        )
    )

    if not inscripciones.exists():

        return Response(
            {
                "error": "No perteneces a este grupo"
            },
            status=404
        )

    grupo = inscripciones.first().asignacion.grupo

    resultado = {
        "grupo": {
            "grupo_id": grupo.id,
            "grupo_nombre": grupo.nombre,
            "instructor_nombre": grupo.profesor.nombre,
            "grado": grupo.grado,
            "jornada": grupo.jornada
        },
        "laboratorios": []
    }

    for inscripcion in inscripciones:

        asignacion = inscripcion.asignacion
        laboratorio = asignacion.laboratorio

        estado_entrega = "PENDIENTE"
        fecha_entrega = None
        nota = None
        calificacion_estado = "SIN_CALIFICAR"

        if hasattr(inscripcion, 'entrega'):

            estado_entrega = inscripcion.entrega.estado
            fecha_entrega = inscripcion.entrega.fecha_entrega

            if hasattr(
                inscripcion.entrega,
                'evaluacion_docente'
            ):

                nota = (
                    inscripcion.entrega
                    .evaluacion_docente
                    .calificacion
                )

                calificacion_estado = "CALIFICADO"

        resultado["laboratorios"].append({

            "asignacion_id": asignacion.id,

            "laboratorio_id": laboratorio.id,

            "titulo": laboratorio.titulo,

            "categoria": (
                laboratorio.plantilla
                .categoria.nombre
            ),

            "estado_asignacion": asignacion.estado,

            "estado_entrega": estado_entrega,

            "fecha_inicio": asignacion.fecha_inicio,

            "fecha_limite": asignacion.fecha_fin,

            "fecha_entrega": fecha_entrega,

            "nota": nota,

            "calificacion_estado":
                calificacion_estado
        })

    return Response(resultado)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_asignacion(request, asignacion_id):

    try:

        inscripcion = (
            Inscripcion.objects
            .select_related(
                'asignacion',
                'asignacion__grupo',
                'asignacion__laboratorio',
                'asignacion__laboratorio__plantilla',
                'entrega',
                'entrega__evaluacion_docente'
            )
            .get(
                estudiante=request.user,
                asignacion_id=asignacion_id
            )
        )

    except Inscripcion.DoesNotExist:

        return Response(
            {
                "error": "No tienes acceso a esta asignación"
            },
            status=404
        )

    asignacion = inscripcion.asignacion
    laboratorio = asignacion.laboratorio

    estado_entrega = None
    fecha_entrega = None
    nota = None

    if hasattr(inscripcion, 'entrega'):

        estado_entrega = inscripcion.entrega.estado
        fecha_entrega = inscripcion.entrega.fecha_entrega

        if hasattr(
            inscripcion.entrega,
            'evaluacion_docente'
        ):
            nota = (
                inscripcion.entrega
                .evaluacion_docente
                .calificacion
            )

    return Response({

        "asignacion_id": asignacion.id,

        "grupo": asignacion.grupo.nombre,

        "estado_entrega": estado_entrega,
        "fecha_entrega": fecha_entrega,
        "fecha_limite": asignacion.fecha_fin,
        "nota": nota,

        "laboratorio": {
            "id": laboratorio.id,
            "titulo": laboratorio.titulo,
            "categoria": laboratorio.plantilla.categoria.nombre,
            "resumen": laboratorio.resumen,
            "introduccion": laboratorio.introduccion,
            "marco_teorico": laboratorio.marco_teorico
        }
    })

# =========================================================
# GRUPO ACADEMICO
# =========================================================
class GruposLaboratoriosView(
    ListAPIView
):

    serializer_class = (
        GrupoLaboratorioSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            Inscripcion.objects
            .filter(
                estudiante=self.request.user
            )
            .select_related(
                'asignacion',
                'asignacion__laboratorio',
                'asignacion__laboratorio__plantilla',
                'asignacion__laboratorio__profesor',
                'entrega',
                'entrega__evaluacion_docente'
            )
        )

