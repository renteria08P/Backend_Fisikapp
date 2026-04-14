from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Log, Notificacion
from .serializers import LogSerializer, NotificacionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Log.objects.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            return Log.objects.none()

        return Log.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notificacion.objects.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            return Notificacion.objects.none()

        return Notificacion.objects.filter(usuario=user)

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