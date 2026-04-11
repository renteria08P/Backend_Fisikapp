from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, recuperar_password, restablecer_password, login_usuario

router = DefaultRouter()
router.register(r'usuarios', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_usuario),
    path('recuperar-password/', recuperar_password),
    path('restablecer-password/', restablecer_password),
]