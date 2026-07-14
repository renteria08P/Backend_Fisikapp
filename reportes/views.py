from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import ReporteLaboratorio
from .serializers import HistorialReporteSerializer
from .filters import HistorialReporteFilter


class HistorialReportesDocenteView(generics.ListAPIView):

    serializer_class = HistorialReporteSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]

    filterset_class = HistorialReporteFilter

    def get_queryset(self):

        # VALIDAR QUE SEA PROFESOR
        if self.request.user.rol != 'profesor':
            return ReporteLaboratorio.objects.none()

        return (
            ReporteLaboratorio.objects
            .filter(
                laboratorio__profesor=self.request.user
            )
            .select_related(
                'laboratorio',
                'laboratorio__plantilla'
            )
            .prefetch_related('estudiantes')
            .distinct()
            .order_by('-fecha_creacion')
        )