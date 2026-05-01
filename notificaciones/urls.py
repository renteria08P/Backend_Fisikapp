from rest_framework.routers import DefaultRouter
from .views import LogViewSet, NotificacionViewSet

router = DefaultRouter()
router.register(r'logs', LogViewSet)
router.register(r'notificaciones', NotificacionViewSet)
