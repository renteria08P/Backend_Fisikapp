from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laboratorios.models import SimulacionAR
from inscripciones.models import GrupoEstudiante

from .ar_serializers import MobileARConfigSerializer


class MobileARConfigAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, ar_id):

        ar_config = get_object_or_404(
            SimulacionAR.objects.select_related(
                "laboratorio",
                "laboratorio__profesor",
            ),
            pk=ar_id,
            enabled=True
        )

        laboratorio = ar_config.laboratorio

        # El estudiante solo puede consultar AR si pertenece
        # a un grupo que tenga asignado este laboratorio.
        if getattr(request.user, "rol", None) == "estudiante":

            pertenece = GrupoEstudiante.objects.filter(
                estudiante=request.user,
                grupo__asignaciones__laboratorio=laboratorio,
                estado="ACTIVO"
            ).exists()

            if not pertenece:
                return Response(
                    {
                        "error": "No tienes acceso a esta simulación AR."
                    },
                    status=403
                )

        serializer = MobileARConfigSerializer(
            ar_config
        )

        return Response(
            serializer.data
        )