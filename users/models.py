from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import json
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError

# =========================================================
# MANAGER PERSONALIZADO
# =========================================================
class UsersManager(BaseUserManager):

    def create_user(self, correo, password=None, **extra_fields):
        """
        Método para crear usuarios normales.
        """
        if not correo:
            raise ValueError('El correo es requerido')

        correo = self.normalize_email(correo)

        # Rol por defecto si no se envía
        extra_fields.setdefault('rol', 'estudiante')

        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """
        Método para crear superusuario (admin Django).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # IMPORTANTE: asignar rol real
        extra_fields.setdefault('rol', 'superadmin')

        return self.create_user(correo, password, **extra_fields)


# =========================================================
# MODELO USUARIO
# =========================================================
class Users(AbstractBaseUser, PermissionsMixin):

    # ROLES DEFINIDOS 
    ROLES = (
    ('superadmin', 'SuperAdmin'),
    ('admin', 'Admin'),
    ('profesor', 'Profesor'),
    ('estudiante', 'Estudiante'),
)

    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    identificacion = models.CharField(max_length=20, unique=True, null=True, blank=True)
    correo = models.EmailField(unique=True)
    institucion = models.CharField(max_length=100, null=True, blank=True)

    # Campo clave de roles
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Foto de perfil con Cloudinary
    foto = CloudinaryField('image', folder='usuarios', null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = Users.objects.get(pk=self.pk)
                if old.foto and old.foto != self.foto:
                    old.foto.delete()  
            except Users.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    # Campo para reconocimiento 
    embedded = models.TextField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.embedded:
            if isinstance(self.embedded, (dict, list)):
                self.embedded = json.dumps(self.embedded)

        super().save(*args, **kwargs)

    # Autorización de tratamiento de datos
    autorizacion_datos = models.BooleanField(default=False)

    # CAMPOS REQUERIDOS POR DJANGO
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    objects = UsersManager()

    def __str__(self):
        return self.nombre

    # =========================================================
    # PERMISOS DJANGO
    # =========================================================

    def has_perm(self, perm, obj=None):
        """
        Permisos individuales.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Permisos por módulo.
        """
        return True