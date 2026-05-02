from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet,
    login_usuario,
    register_user,
    user_profile,
    change_password,
    recuperar_password,
    restablecer_password,
    crear_admin,
    crear_profesor
)

router = DefaultRouter()
router.register(r'usuarios', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # AUTH PUBLICO
    path('register/', register_user),
    path('login/', login_usuario),


     # PERFIL (LOGIN REQUIRED)
    path('perfil/', user_profile),  
    path('change-password/', change_password), 


    # ROLES
    path('crear-admin/', crear_admin),
    path('crear-profesor/', crear_profesor),


    # RECUPERACIÓN
    path('recuperar-contrasena/', recuperar_password),
    path('restablecer-contrasena/', restablecer_password),
]