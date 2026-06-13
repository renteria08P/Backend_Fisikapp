from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    EvaluacionProfesor,
    EvaluacionIA
)

from .serializers import (
    EvaluacionProfesorSerializer,
    EvaluacionIASerializer
)


class EvaluacionProfesorViewSet(
    ModelViewSet
):

    queryset = (
        EvaluacionProfesor.objects.all()
    )

    serializer_class = (
        EvaluacionProfesorSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer
    ):
        serializer.save(
            profesor=self.request.user
        )


class EvaluacionIAViewSet(
    ModelViewSet
):

    queryset = (
        EvaluacionIA.objects.all()
    )

    serializer_class = (
        EvaluacionIASerializer
    )

    permission_classes = [
        IsAuthenticated
    ]