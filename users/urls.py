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
    crear_profesor,
    TotalEstudiantesAPIView, 
)

router = DefaultRouter()
router.register(r'usuarios', UsersViewSet)

urlpatterns = [

    
    # RECUPERACIÓN
    path('recuperar-contrasena/', recuperar_password),
    path('restablecer-contrasena/', restablecer_password),

    
    # AUTH PUBLICO
    path('register/', register_user),
    path('login/', login_usuario),


    path('', include(router.urls)),

    # PERFIL (LOGIN REQUIRED)
    path('perfil/', user_profile),  
    path('change-password/', change_password), 


    # ROLES
    path('crear-admin/', crear_admin),
    path('crear-profesor/', crear_profesor),


    # DASHBOARD
    path(
        'dashboard/total-estudiantes/',
        TotalEstudiantesAPIView.as_view(),
        name='total-estudiantes',
    ),
]