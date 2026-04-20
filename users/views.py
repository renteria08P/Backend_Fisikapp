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
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .permissions import IsAdminOrSuperAdmin # PERMISOS PERSONALIZADOS


# =========================================================
#CRUD DE USUARIOS (SOLO ADMIN)
# =========================================================
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    # Solo admin puede gestionar usuarios
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    # Permite subir imágenes (foto perfil)
    parser_classes = [MultiPartParser, FormParser,JSONParser]

    @swagger_auto_schema(tags=['users'])
    def list(self, request, *args, **kwargs):
        """Listar todos los usuarios"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['users'])
    def create(self, request, *args, **kwargs):
        """Crear usuario (solo admin)"""
        print("DATA RECIBIDA:", request.data)
        s = UsersSerializer(data=request.data)
        print("VALIDO:", s.is_valid())
        print("ERRORES:", s.errors)
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
    
    def perform_create(self, serializer):
        rol = self.request.data.get('rol', 'estudiante')
        serializer.save(rol=rol)


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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirmar_password = request.data.get('confirmar_password')

    # Validar campos
    if not old_password or not new_password or not confirmar_password:
        return Response({"error": "Todos los campos son requeridos"}, status=400)

    # Validar contraseña actual
    if not user.check_password(old_password):
        return Response({"error": "Contraseña actual incorrecta"}, status=400)

    # Validar que coincidan
    if new_password != confirmar_password:
        return Response({"error": "Las contraseñas no coinciden"}, status=400)

    # Validaciones de seguridad
    import re
    if len(new_password) < 8:
        return Response({"error": "Mínimo 8 caracteres"}, status=400)
    if not re.search(r"[A-Z]", new_password):
        return Response({"error": "Debe tener una mayúscula"}, status=400)
    if not re.search(r"[0-9]", new_password):
        return Response({"error": "Debe tener un número"}, status=400)

    # Evitar misma contraseña
    if user.check_password(new_password):
        return Response({"error": "La nueva contraseña no puede ser igual a la anterior"}, status=400)

    # Guardar
    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña actualizada correctamente"})

# =========================================================
# RECUPERAR PASSWORD
# =========================================================
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

token_generator = PasswordResetTokenGenerator()

@api_view(['POST'])
def recuperar_password(request):
    correo = request.data.get('correo')

    if not correo:
        return Response({"error": "Correo es requerido"}, status=400)

    try:
        user = Users.objects.get(correo=correo)
    except Users.DoesNotExist:
        # Seguridad: no revelar si existe o no
        return Response({"message": "Si el correo existe, se enviará un enlace"})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    # BACKEND (actual)
    reset_link = f"http://127.0.0.1:8000/api/users/restablecer-password/?uid={uid}&token={token}"

    # FRONT (futuro)
    # reset_link = f"http://localhost:5173/reset-password?uid={uid}&token={token}"

    html_content = render_to_string('emails/reset_password.html', {
        'user': user,
        'reset_link': reset_link
    })

    email = EmailMultiAlternatives(
        subject='Recuperación de contraseña - FisikApp',
        body='Usa un cliente compatible con HTML',
        from_email='FisikApp <fisikapp7@gmail.com>',
        to=[correo],
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return Response({"message": "Si el correo existe, se enviará un enlace"})
# =========================================================
# RESTABLECER PASSWORD
# =========================================================
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
import re

@api_view(['POST'])
def restablecer_password(request):
    uid = request.query_params.get('uid')
    token = request.query_params.get('token')
    new_password = request.data.get('new_password')

    if not uid or not token:
        return Response({"error": "Datos inválidos"}, status=400)

    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = Users.objects.get(pk=uid_decoded)
    except:
        return Response({"error": "Usuario inválido"}, status=400)

    if not token_generator.check_token(user, token):
        return Response({"error": "Token inválido o expirado"}, status=400)

    if not new_password:
        return Response({"error": "Nueva contraseña requerida"}, status=400)

    # Validación fuerte
    if len(new_password) < 8:
        return Response({"error": "Mínimo 8 caracteres"}, status=400)
    if not re.search(r"[A-Z]", new_password):
        return Response({"error": "Debe tener una mayúscula"}, status=400)
    if not re.search(r"[0-9]", new_password):
        return Response({"error": "Debe tener un número"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña restablecida correctamente"})

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