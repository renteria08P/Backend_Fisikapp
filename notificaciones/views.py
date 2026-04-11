from rest_framework import viewsets
from .models import Log, Notificacion
from .serializers import LogSerializer, NotificacionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer

    def get_queryset(self):
        return Log.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()

        if notificacion.usuario != request.user:
            return Response({"error": "No autorizado"}, status=403)

        notificacion.estado = True
        notificacion.save()

        return Response({"mensaje": "Notificación marcada como leída"})