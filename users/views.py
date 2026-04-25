from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import Users
from .serializers import UsersSerializer, LoginSerializer
from .permissions import IsAdminOrSuperAdmin
from .utils import generar_password, enviar_credenciales

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import re

token_generator = PasswordResetTokenGenerator()


# =========================================================
# USERS 
# =========================================================
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all() 
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get_queryset(self):
        roles = self.request.query_params.getlist('rol')
        if roles:
            return Users.objects.filter(rol__in=roles)
        return Users.objects.all()

    def perform_create(self, serializer):
        rol = self.request.data.get('rol', 'estudiante')
        serializer.save(rol=rol)


# =========================================================
# LOGIN
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    correo = serializer.validated_data['correo']
    password = serializer.validated_data['password']

    try:
        user = Users.objects.get(correo=correo)

        if not check_password(password, user.password):
            return Response({"error": "Credenciales inválidas"}, status=400)

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

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
        return Response({"error": "Credenciales inválidas"}, status=404)


# =========================================================
# PERFIL
# =========================================================
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser]) 
def user_profile(request):

    user = request.user

    if request.method == 'GET':
        return Response(UsersSerializer(user).data)

    print("DATA PERFIL:", request.data)
    print("FILES:", request.FILES)

    serializer = UsersSerializer(user, data=request.data, partial=True)

    print("VALIDO:", serializer.is_valid())
    print("ERRORES:", serializer.errors)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Perfil actualizado",
            "data": serializer.data
        })

    return Response(serializer.errors, status=400)


# =========================================================
# CAMBIO PASSWORD
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user

    old = request.data.get('old_password')
    new = request.data.get('new_password')
    confirm = request.data.get('confirmar_password')

    if not all([old, new, confirm]):
        return Response({"error": "Campos requeridos"}, status=400)

    if not user.check_password(old):
        return Response({"error": "Contraseña actual incorrecta"}, status=400)

    if new != confirm:
        return Response({"error": "No coinciden"}, status=400)

    if len(new) < 8:
        return Response({"error": "Mínimo 8 caracteres"}, status=400)

    if not re.search(r"[A-Z]", new):
        return Response({"error": "Debe tener mayúscula"}, status=400)

    if not re.search(r"[0-9]", new):
        return Response({"error": "Debe tener número"}, status=400)

    if user.check_password(new):
        return Response({"error": "No puede ser igual"}, status=400)

    user.set_password(new)
    user.save()

    return Response({"message": "Contraseña actualizada"})


# =========================================================
# REGISTER
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser]) 
def register_user(request):

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='estudiante')
        return Response({"message": "Usuario registrado"}, status=201)

    return Response(serializer.errors, status=400)


# =========================================================
# CREAR ADMIN (PROTEGIDO CORRECTAMENTE)
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrSuperAdmin])
def crear_admin(request):

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(rol='admin')
        return Response({"message": "Admin creado"})

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

        return Response({"message": "Profesor creado"})

    return Response(serializer.errors, status=400)


# =========================================================
# RECUPERAR PASSWORD
# =========================================================
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

@api_view(['POST'])
@permission_classes([AllowAny])
def recuperar_password(request):

    correo = request.data.get('correo')

    if not correo:
        return Response({"error": "Correo requerido"}, status=400)

    try:
        user = Users.objects.get(correo=correo)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_link = f"http://127.0.0.1:8000/reset-password/?uid={uid}&token={token}"

        html = render_to_string('emails/reset_password.html', {
            'user': user,
            'reset_link': reset_link
        })

        message = Mail(
            from_email='fisikapp7@gmail.com',  
            to_emails=correo,
            subject='Recuperar contraseña',
            html_content=html
        )

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)

        print("STATUS:", response.status_code)

    except Users.DoesNotExist:
        print("Usuario no existe")

    except Exception as e:
        print("ERROR:", str(e))

    return Response({"message": "Si existe, se enviará correo"})


# =========================================================
# RESET PASSWORD
# =========================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def restablecer_password(request):

    uid = request.query_params.get('uid')
    token = request.query_params.get('token')
    new_password = request.data.get('new_password')

    if not all([uid, token, new_password]):
        return Response({"error": "Datos inválidos"}, status=400)

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = Users.objects.get(pk=user_id)

    except:
        return Response({"error": "Usuario inválido"}, status=400)

    if not token_generator.check_token(user, token):
        return Response({"error": "Token inválido"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña restablecida"})