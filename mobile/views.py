from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from laboratorios.models import Asignacion
from .builders.mobile_resource_builder import MobileResourceBuilder
from .simulation.config_builder import SimulationConfigBuilder
from .simulation.serializers import SimulationResultSerializer
from .simulation.result_builder import ResultBuilder

from inscripciones.models import (
    Inscripcion,
    GrupoEstudiante,
)


# =========================================================
# MOBILE RESOURCE
# =========================================================

class MobileResourceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, assignment_id):

        assignment = get_object_or_404(
            Asignacion.objects.select_related(
                "grupo",
                "laboratorio",
                "laboratorio__plantilla",
                "laboratorio__profesor",
                "laboratorio__plantilla__categoria",
            ),
            pk=assignment_id
        )

        # ==========================================
        # VALIDAR QUE EL ESTUDIANTE PERTENECE AL GRUPO
        # ==========================================
        if not GrupoEstudiante.objects.filter(
            estudiante=request.user,
            grupo_id=assignment.grupo_id,
            estado="ACTIVO",
            grupo__activo=True
        ).exists():

            return Response(
                {
                    "error": "No tienes acceso a este laboratorio."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        builder = MobileResourceBuilder(
            assignment
        )

        return Response(builder.build())


# =========================================================
# SIMULATION CONFIG
# =========================================================

class SimulationConfigAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, assignment_id):

        assignment = get_object_or_404(
            Asignacion.objects.select_related(
                "grupo",
                "laboratorio",
            ),
            pk=assignment_id
        )

        if not GrupoEstudiante.objects.filter(
            estudiante=request.user,
            grupo_id=assignment.grupo_id,
            estado="ACTIVO",
            grupo__activo=True
        ).exists():

            return Response(
                {
                    "error": "No tienes acceso a esta simulación."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        data = SimulationConfigBuilder(
            assignment
        ).build()

        return Response(data)


# =========================================================
# SIMULATION RESULT
# =========================================================

class SimulationResultAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, assignment_id):

        inscripcion = get_object_or_404(
            Inscripcion.objects.select_related(
                "estudiante",
                "asignacion",
            ),
            asignacion_id=assignment_id,
            estudiante=request.user
        )

        serializer = SimulationResultSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        builder = ResultBuilder(
            inscripcion,
            serializer.validated_data
        )

        builder.build()

        return Response(
            {
                "message": "Resultado registrado correctamente."
            },
            status=status.HTTP_201_CREATED
        )