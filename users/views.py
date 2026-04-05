from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Users
from .serializers import UsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from .serializers import LoginSerializer

class RegisterSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    correo = serializers.EmailField()
    password = serializers.CharField()
    estado = serializers.BooleanField()

#  CRUD COMPLETO
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


#  REGISTRAR USUARIO
@api_view(['POST'])
def registrar_usuario(request):
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario creado"})

    return Response(serializer.errors)

#  RECUPERAR PASSWORD
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


#  RESTABLECER PASSWORD
@api_view(['POST'])
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
    
@swagger_auto_schema(method='post', request_body=LoginSerializer)
@api_view(['POST'])
def login_usuario(request):
    correo = request.data.get('correo')
    password = request.data.get('password')
    
    if not correo or not password:
        return Response({"error": "Correo y contraseña son requeridos"})

    try:
        user = Users.objects.get(correo=correo)

        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta"}, status=400)

        # Crear tokens
        refresh = RefreshToken()
        refresh['user_id'] = user.id
        refresh['correo'] = user.correo

        return Response({
            "message": "Login exitoso",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"})