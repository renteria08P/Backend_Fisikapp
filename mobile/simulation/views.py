from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from laboratorios.models import Asignacion
from .config_builder import SimulationConfigBuilder
from rest_framework import status
from inscripciones.models import Inscripcion
from .result_builder import ResultBuilder


class SimulationConfigAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, assignment_id):

        assignment = get_object_or_404(
            Asignacion.objects.select_related(
                "laboratorio",
            ),
            pk=assignment_id
        )

        data = SimulationConfigBuilder(
            assignment
        ).build()

        return Response(data)
    
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from inscripciones.models import Inscripcion

from .serializers import SimulationResultSerializer
from .result_builder import ResultBuilder


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
