from rest_framework.routers import DefaultRouter
from .views import LogViewSet, NotificacionViewSet

router = DefaultRouter()

router.register('logs', LogViewSet, basename='logs')
router.register('notificaciones', NotificacionViewSet, basename='notificaciones')