from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from .serializers import UsersSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers



# CRUD COMPLETO
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        password = self.request.data.get('password')
        if password:
            serializer.save(password=make_password(password))
        else:
            serializer.save()

    #  Swagger tags para TODO el CRUD
    @swagger_auto_schema(tags=['Usuarios'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# LOGIN USUARIO 

@swagger_auto_schema(method='post', request_body=LoginSerializer, tags=['Usuarios'])
@api_view(['POST'])
def login_usuario(request):
    correo = request.data.get('correo')
    password = request.data.get('password')

    if not correo or not password:
        return Response({"error": "Correo y contraseña son requeridos"})

    try:
        user = Users.objects.get(correo=correo)

        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta"})

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login exitoso",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"})


#  RECUPERAR PASSWORD
class RecuperarPasswordSerializer(serializers.Serializer):
    correo=serializers.EmailField()
@swagger_auto_schema(method='post', request_body=RecuperarPasswordSerializer, tags=['Usuarios'])
@api_view(['POST'])
def recuperar_password(request):
    correo = request.data.get('correo')

    if not correo:
        return Response({"error": "Correo es requerido"})

    try:
        user = Users.objects.get(correo=correo)
        return Response({
            "message": "Usuario encontrado",
            "user_id": user.id
        })
    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"})


# RESTABLECER PASSWORD
class RestablecerPasswordSerializer(serializers.Serializer):
    user_id=serializers.IntegerField()
    password= serializers.CharField()
@swagger_auto_schema(method='patch', request_body=RestablecerPasswordSerializer, tags=['Usuarios'])
@api_view(['PATCH'])
def restablecer_password(request):
    user_id = request.data.get('user_id')
    nueva_password = request.data.get('password')

    if not user_id or not nueva_password:
        return Response({"error": "user_id y password son requeridos"})

    try:
        user = Users.objects.get(id=user_id)
        user.password = make_password(nueva_password)
        user.save()

        return Response({"message": "Contraseña actualizada"})
    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"})