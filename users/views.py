from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from .serializers import UsersSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsAdmin, IsSuperAdmin, IsAdminOrSuperAdmin # PERMISOS PERSONALIZADOS


# =========================================================
#CRUD DE USUARIOS (SOLO ADMIN)
# =========================================================
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    # Solo admin puede gestionar usuarios
    permission_classes = [IsAuthenticated, IsAdmin]

    # Permite subir imágenes (foto perfil)
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(tags=['users'])
    def list(self, request, *args, **kwargs):
        """Listar todos los usuarios"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def create(self, request, *args, **kwargs):
        """Crear usuario (solo admin)"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def retrieve(self, request, *args, **kwargs):
        """Obtener usuario por ID"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def update(self, request, *args, **kwargs):
        """Actualizar usuario"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def destroy(self, request, *args, **kwargs):
        """Eliminar usuario"""
        return super().destroy(request, *args, **kwargs)


# =========================================================
# LOGIN
# =========================================================
@swagger_auto_schema(method='post', request_body=LoginSerializer, tags=['users'])
@api_view(['POST'])
def login_usuario(request):
    """
    Autenticación de usuario.
    Retorna token JWT si las credenciales son correctas.
    """
    correo = request.data.get('correo')
    password = request.data.get('password')

    if not correo or not password:
        return Response(
            {"error": "Correo y contraseña son requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = Users.objects.get(correo=correo)

        if not check_password(password, user.password):
            return Response(
                {"error": "Contraseña incorrecta"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generación de tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login exitoso",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "nombre": user.nombre,
                "correo": user.correo,
                "rol": user.rol,
            }
        })

    except Users.DoesNotExist:
        return Response(
            {"error": "Usuario no existe"},
            status=status.HTTP_404_NOT_FOUND
        )


# =========================================================
# PERFIL DE USUARIO
# =========================================================
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    GET: Obtener perfil del usuario autenticado
    PATCH: Actualizar datos del perfil
    """
    user = request.user

    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = UsersSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Perfil actualizado",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# CAMBIO DE CONTRASEÑA
# =========================================================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Permite al usuario cambiar su contraseña validando la actual.
    """
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"error": "Contraseña actual incorrecta"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"message": "Contraseña actualizada correctamente"})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# RECUPERAR PASSWORD
# =========================================================
@api_view(['POST'])
def recuperar_password(request):
    """
    Verifica si el correo existe para iniciar recuperación.
    """
    correo = request.data.get('correo')

    if not correo:
        return Response({"error": "Correo es requerido"}, status=400)

    try:
        user = Users.objects.get(correo=correo)
        return Response({
            "message": "Usuario encontrado",
            "user_id": user.id
        })
    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"}, status=404)


# =========================================================
# RESTABLECER PASSWORD
# =========================================================
@api_view(['PATCH'])
def restablecer_password(request):
    """
    Cambia la contraseña usando el user_id.
    """
    user_id = request.data.get('user_id')
    nueva_password = request.data.get('password')

    if not user_id or not nueva_password:
        return Response({"error": "Datos requeridos"}, status=400)

    try:
        user = Users.objects.get(id=user_id)
        user.set_password(nueva_password)
        user.save()

        return Response({"message": "Contraseña actualizada"})
    except Users.DoesNotExist:
        return Response({"error": "Usuario no existe"}, status=404)


# =========================================================
# REGISTRO DE USUARIO
# =========================================================
@swagger_auto_schema(
    method='post',
    operation_description="Registro de usuario",
    tags=['users']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registro público:
    Siempre crea usuarios con rol = estudiante
    No permite elegir rol (seguridad)
    """
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='estudiante') 
        return Response({
            "message": "Usuario registrado correctamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# CREAR ADMIN (SOLO SUPERADMIN)
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def crear_admin(request):
    print("ENTRO A LA VISTA")
    print("CONTENT TYPE:", request.content_type)
    print("BODY:", request.body)
    print("DATA:", request.data)

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='admin')
        return Response({
            "message": "Admin creado",
            "data": serializer.data
        })

    print("ERRORES:", serializer.errors)
    return Response(serializer.errors, status=400)


# =========================================================
# CREAR PROFESOR (ADMIN O SUPERADMIN)
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrSuperAdmin])
def crear_profesor(request):
    """
    Admin y superadmin pueden crear profesores.
    """

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='profesor')
        return Response({
            "message": "Profesor creado",
            "data": serializer.data
        })


    return Response(serializer.errors, status=400)