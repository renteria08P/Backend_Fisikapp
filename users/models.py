from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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

    # Foto de perfil
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)

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