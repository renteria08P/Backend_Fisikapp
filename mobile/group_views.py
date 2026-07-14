from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from laboratorios.models import GrupoAcademico, Asignacion
from inscripciones.models import GrupoEstudiante, Inscripcion

from .group_serializers import JoinGroupRequestSerializer


def es_estudiante(user):
    return getattr(user, "rol", None) == "estudiante"


def obtener_entrega_de_usuario(user, asignacion):
    inscripcion = (
        Inscripcion.objects
        .filter(
            estudiante=user,
            asignacion=asignacion
        )
        .select_related("entrega")
        .first()
    )

    if not inscripcion:
        return None, None

    entrega = getattr(inscripcion, "entrega", None)

    return inscripcion, entrega


def obtener_estado_entrega(entrega):
    if not entrega:
        return "PENDIENTE"

    return entrega.estado


def obtener_notas(entrega):
    if not entrega:
        return None, None, "SIN_ENTREGA"

    evaluacion_ia = getattr(entrega, "evaluacion_ia", None)
    evaluacion_docente = getattr(entrega, "evaluacion_docente", None)

    nota_ia = (
        float(evaluacion_ia.calificacion)
        if evaluacion_ia
        else None
    )

    nota_docente = (
        float(evaluacion_docente.calificacion)
        if evaluacion_docente
        else None
    )

    if evaluacion_docente:
        estado = "CALIFICADO_DOCENTE"
    elif evaluacion_ia:
        estado = "PENDIENTE_REVISION_DOCENTE"
    elif entrega.estado == "ENVIADA":
        estado = "PENDIENTE_EVALUACION_IA"
    else:
        estado = "SIN_CALIFICAR"

    return nota_ia, nota_docente, estado


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_group(request):
    """
    Nuevo flujo móvil:
    Código de grupo -> estudiante pertenece al grupo.
    No crea Inscripcion a asignaciones todavía.
    """

    if not es_estudiante(request.user):
        return Response(
            {
                "error": "Solo los estudiantes pueden unirse a grupos."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = JoinGroupRequestSerializer(
        data=request.data
    )

    serializer.is_valid(
        raise_exception=True
    )

    codigo = (
        serializer.validated_data["codigo"]
        .strip()
        .upper()
    )

    grupo = get_object_or_404(
        GrupoAcademico,
        codigo_ingreso=codigo,
        activo=True
    )

    relacion, creado = GrupoEstudiante.objects.get_or_create(
        estudiante=request.user,
        grupo=grupo,
        defaults={
            "estado": "ACTIVO"
        }
    )

    if not creado and relacion.estado != "ACTIVO":
        relacion.estado = "ACTIVO"
        relacion.save(update_fields=["estado"])

    total_laboratorios = Asignacion.objects.filter(
        grupo=grupo
    ).count()

    laboratorios_activos = Asignacion.objects.filter(
        #grupo=grupo,
        estado="ACTIVO"
    ).count()

    return Response(
        {
            "message": (
                "Inscripción al grupo realizada correctamente."
                if creado
                else "Ya perteneces a este grupo."
            ),
            "created": creado,
            "grupo": {
                "grupo_id": grupo.id,
                "grupo_nombre": grupo.nombre,
                "grado": grupo.grado,
                "jornada": grupo.jornada,
                "instructor_nombre": grupo.profesor.nombre,
                "total_laboratorios": total_laboratorios,
                "laboratorios_activos": laboratorios_activos,
            }
        },
        status=status.HTTP_201_CREATED if creado else status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_groups(request):
    """
    Nuevo dashboard móvil:
    Devuelve grupos reales del estudiante desde GrupoEstudiante.
    """

    if not es_estudiante(request.user):
        return Response(
            {
                "error": "Solo los estudiantes pueden consultar sus grupos."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    relaciones = (
        GrupoEstudiante.objects
        .filter(
            estudiante=request.user,
            estado="ACTIVO"
        )
        .select_related(
            "grupo",
            "grupo__profesor"
        )
    )

    resultado = []

    for relacion in relaciones:
        grupo = relacion.grupo

        asignaciones = (
            Asignacion.objects
            .filter(grupo=grupo)
            .select_related(
                "laboratorio",
                "laboratorio__plantilla"
            )
        )

        total_laboratorios = asignaciones.count()

        asignaciones_activas = asignaciones.filter(
            estado="ACTIVO"
        )

        laboratorios_activos = asignaciones_activas.count()

        entregas_pendientes = 0
        entregas_enviadas = 0
        calificaciones_pendientes = 0

        for asignacion in asignaciones_activas:
            _, entrega = obtener_entrega_de_usuario(
                request.user,
                asignacion
            )

            if not entrega:
                entregas_pendientes += 1
                continue

            if entrega.estado == "ENVIADA":
                entregas_enviadas += 1
                calificaciones_pendientes += 1

            if entrega.estado not in [
                "APROBADO",
                "APROBADA",
                "RECHAZADO",
                "RECHAZADA",
                "REVISADA_DOCENTE"
            ]:
                entregas_pendientes += 1

        resultado.append(
            {
                "grupo_id": grupo.id,
                "grupo_nombre": grupo.nombre,
                "grado": grupo.grado,
                "jornada": grupo.jornada,
                "instructor_nombre": grupo.profesor.nombre,

                "total_laboratorios": total_laboratorios,
                "laboratorios_activos": laboratorios_activos,

                "entregas_pendientes": entregas_pendientes,
                "entregas_enviadas": entregas_enviadas,
                "calificaciones_pendientes": calificaciones_pendientes,
            }
        )

    return Response(resultado)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def group_assignments(request, grupo_id):
    """
    Nuevo flujo móvil:
    Devuelve todas las asignaciones activas del grupo
    si el estudiante pertenece al grupo.
    """

    if not es_estudiante(request.user):
        return Response(
            {
                "error": "Solo los estudiantes pueden consultar asignaciones."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    relacion = GrupoEstudiante.objects.filter(
        estudiante=request.user,
        grupo_id=grupo_id,
        estado="ACTIVO"
    ).select_related("grupo").first()

    if not relacion:
        return Response(
            {
                "error": "No perteneces a este grupo."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    grupo = relacion.grupo

    asignaciones = (
        Asignacion.objects
        .filter(
            grupo=grupo,
            estado="ACTIVO"
        )
        .select_related(
            "grupo",
            "laboratorio",
            "laboratorio__profesor",
            "laboratorio__plantilla",
            "laboratorio__plantilla__categoria",
        )
        .order_by("fecha_fin")
    )

    laboratorios = []

    for asignacion in asignaciones:
        laboratorio = asignacion.laboratorio
        plantilla = laboratorio.plantilla

        _, entrega = obtener_entrega_de_usuario(
            request.user,
            asignacion
        )

        estado_entrega = obtener_estado_entrega(entrega)
        nota_ia, nota_docente, calificacion_estado = obtener_notas(
            entrega
        )

        #lab_key = plantilla.lab_key
        lab_key = getattr(plantilla, "lab_key", None)
        
        categoria_nombre = None

        if plantilla.categoria:
            categoria_nombre = plantilla.categoria.nombre

        laboratorios.append(
            {
                "asignacion_id": asignacion.id,
                "laboratorio_id": laboratorio.id,

                "titulo": laboratorio.titulo,
                "categoria": categoria_nombre,
                "instructor_nombre": laboratorio.profesor.nombre,

                "estado_asignacion": asignacion.estado,
                "estado_entrega": estado_entrega,

                "fecha_inicio": asignacion.fecha_inicio,
                "fecha_limite": asignacion.fecha_fin,
                "fecha_entrega": entrega.fecha_entrega if entrega else None,

                "tiene_ar": bool(lab_key),
                "lab_key": lab_key,

                "nota_ia": nota_ia,
                "nota_docente": nota_docente,
                "calificacion_estado": calificacion_estado,

                "resource_endpoint": (
                    f"/api/mobile/resources/{asignacion.id}/"
                )
            }
        )

    return Response(
        {
            "grupo": {
                "grupo_id": grupo.id,
                "grupo_nombre": grupo.nombre,
                "grado": grupo.grado,
                "jornada": grupo.jornada,
                "instructor_nombre": grupo.profesor.nombre,
            },
            "laboratorios": laboratorios
        }
    )