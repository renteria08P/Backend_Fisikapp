from django.urls import path
from notificaciones.routing import websocket_urlpatterns
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path(
        "ws/notificaciones/",
        NotificationConsumer.as_asgi(),
    ),
]