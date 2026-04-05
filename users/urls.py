from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, registrar_usuario, recuperar_password, restablecer_password
from .views import login_usuario

router = DefaultRouter()
router.register(r'usuarios', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registrar/', registrar_usuario),
    path('recuperar-password/', recuperar_password),
    path('restablecer-password/', restablecer_password),
    path('login/', login_usuario),
]