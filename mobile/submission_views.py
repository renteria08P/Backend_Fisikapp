from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from laboratorios.models import Asignacion
from inscripciones.models import (
    Inscripcion,
    GrupoEstudiante,
)

from entregas.models import (
    Entrega,
    EntregaLaboratorioUnificada,
)

from .submission_serializers import (
    MobileUnifiedSubmissionSerializer,
)

from .llm_payload_builder import LLMPayloadBuilder


def estudiante_tiene_acceso_asignacion(user, asignacion):

    if getattr(user, "rol", None) != "estudiante":
        return False

    return GrupoEstudiante.objects.filter(
        estudiante=user,
        grupo=asignacion.grupo,
        estado="ACTIVO"
    ).exists()


class MobileUnifiedSubmissionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, assignment_id):

        asignacion = get_object_or_404(
            Asignacion.objects.select_related(
                "grupo",
                "laboratorio",
                "laboratorio__plantilla",
                "laboratorio__plantilla__categoria",
                "laboratorio__profesor",
            ),
            pk=assignment_id,
            estado="ACTIVO"
        )

        if not estudiante_tiene_acceso_asignacion(
            request.user,
            asignacion
        ):
            return Response(
                {
                    "error": "No tienes acceso a esta asignación."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MobileUnifiedSubmissionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        submission_data = serializer.validated_data

        inscripcion, _ = Inscripcion.objects.get_or_create(
            estudiante=request.user,
            asignacion=asignacion
        )

        entrega, _ = Entrega.objects.update_or_create(
            inscripcion=inscripcion,
            defaults={
                "tipo_reporte": "INTEGRADA",
                "estado": "ENVIADA",
                "fecha_entrega": timezone.now(),
            }
        )

        llm_payload = LLMPayloadBuilder(
            user=request.user,
            assignment=asignacion,
            submission_data=submission_data
        ).build()

        entrega_unificada, _ = (
            EntregaLaboratorioUnificada.objects
            .update_or_create(
                entrega=entrega,
                defaults={
                    "practice": submission_data.get(
                        "practice",
                        {}
                    ),
                    "simulation": submission_data.get(
                        "simulation",
                        {}
                    ),
                    "comparison": submission_data.get(
                        "comparison",
                        {}
                    ),
                    "questions": submission_data.get(
                        "questions",
                        []
                    ),
                    "report": submission_data.get(
                        "report",
                        {}
                    ),
                    "device": submission_data.get(
                        "device",
                        {}
                    ),
                    "llm_payload": llm_payload,
                    "raw_payload": request.data,
                }
            )
        )

        return Response(
            {
                "message": "Entrega enviada correctamente.",
                "assignment_id": asignacion.id,
                "entrega_id": entrega.id,
                "entrega_unificada_id": entrega_unificada.id,
                "estado": entrega.estado,
                "tipo_reporte": entrega.tipo_reporte,
                "fecha_entrega": entrega.fecha_entrega,
                "requires_ai_evaluation": True,
                "requires_teacher_review": True,
            },
            status=status.HTTP_201_CREATED
        )