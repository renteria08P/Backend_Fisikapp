
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from users.permissions import IsProfesor, Roles

from .models import (
    EvaluacionProfesor,
    EvaluacionIA
)

from .serializers import (
    EvaluacionProfesorSerializer,
    EvaluacionIASerializer
)


class EvaluacionProfesorViewSet(ModelViewSet):

    serializer_class = EvaluacionProfesorSerializer

    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return EvaluacionProfesor.objects.filter(
                entrega__inscripcion__estudiante=self.request.user
            )

        return EvaluacionProfesor.objects.all()

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsProfesor()
        ]

    def perform_create(self, serializer):

        entrega = serializer.validated_data["entrega"]

        if (
            entrega.inscripcion.asignacion.laboratorio.profesor
            != self.request.user
        ):
            raise ValidationError(
                "No puedes evaluar un laboratorio que no te pertenece."
            )

        serializer.save(
            profesor=self.request.user
        )



class EvaluacionIAViewSet(ReadOnlyModelViewSet):

    serializer_class = EvaluacionIASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.rol == Roles.ESTUDIANTE:
            return EvaluacionIA.objects.filter(
                entrega__inscripcion__estudiante=self.request.user
            )

        return EvaluacionIA.objects.all()
