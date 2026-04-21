from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from .serializers import UsersSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAdminOrSuperAdmin
from .utils import generar_password, enviar_credenciales

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import re

token_generator = PasswordResetTokenGenerator()


# =========================================================
# CRUD USUARIOS
# =========================================================
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        rol = self.request.data.get('rol', 'estudiante')
        serializer.save(rol=rol)


# =========================================================
# LOGIN
# =========================================================
@swagger_auto_schema(method='post', request_body=LoginSerializer, tags=['users'])
@api_view(['POST'])
def login_usuario(request):
    correo = request.data.get('correo')
    password = request.data.get('password')

    if not correo or not password:
        return Response({"error": "Correo y contraseña son requeridos"}, status=400)

    try:
        user = Users.objects.get(correo=correo)

        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta"}, status=400)

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
        return Response({"error": "Usuario no existe"}, status=404)


# =========================================================
# PERFIL
# =========================================================
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
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

        return Response(serializer.errors, status=400)


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

    if not old_password or not new_password or not confirmar_password:
        return Response({"error": "Todos los campos son requeridos"}, status=400)

    if not user.check_password(old_password):
        return Response({"error": "Contraseña actual incorrecta"}, status=400)

    if new_password != confirmar_password:
        return Response({"error": "Las contraseñas no coinciden"}, status=400)

    if len(new_password) < 8:
        return Response({"error": "Mínimo 8 caracteres"}, status=400)
    if not re.search(r"[A-Z]", new_password):
        return Response({"error": "Debe tener una mayúscula"}, status=400)
    if not re.search(r"[0-9]", new_password):
        return Response({"error": "Debe tener un número"}, status=400)

    if user.check_password(new_password):
        return Response({"error": "No puede ser igual a la anterior"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña actualizada correctamente"})


# =========================================================
# REGISTRO
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='estudiante')

        return Response({
            "message": "Usuario registrado correctamente",
            "data": serializer.data
        }, status=201)

    return Response(serializer.errors, status=400)


# =========================================================
# CREAR ADMIN
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def crear_admin(request):

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='admin')

        return Response({
            "message": "Admin creado",
            "data": serializer.data
        })

    return Response(serializer.errors, status=400)


# =========================================================
# CREAR PROFESOR
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrSuperAdmin])
def crear_profesor(request):

    data = request.data.copy()

    password = generar_password()
    data['password'] = password

    serializer = UsersSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save(rol='profesor')

        enviar_credenciales(user, password)

        return Response({
            "message": "Profesor creado",
            "data": serializer.data
        })

    return Response(serializer.errors, status=400)


# =========================================================
# RECUPERAR PASSWORD
# =========================================================
@api_view(['POST'])
def recuperar_password(request):
    correo = request.data.get('correo')

    if not correo:
        return Response({"error": "Correo es requerido"}, status=400)

    try:
        user = Users.objects.get(correo=correo)
    except Users.DoesNotExist:
        return Response({"message": "Si el correo existe, se enviará un enlace"})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    reset_link = f"http://127.0.0.1:8000/api/users/restablecer-password/?uid={uid}&token={token}"

    html_content = render_to_string('emails/reset_password.html', {
        'user': user,
        'reset_link': reset_link
    })

    email = EmailMultiAlternatives(
        subject='Recuperación de contraseña',
        body='HTML required',
        from_email='FisikApp <fisikapp7@gmail.com>',
        to=[correo],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    return Response({"message": "Si el correo existe, se enviará un enlace"})


# =========================================================
# RESTABLECER PASSWORD
# =========================================================
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
        return Response({"error": "Token inválido"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña restablecida correctamente"})