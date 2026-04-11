from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsersManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es requerido')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        return self.create_user(correo, password, **extra_fields)

class Users(AbstractBaseUser):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    identificacion = models.CharField(max_length=20, unique=True, null=True, blank=True)
    correo = models.EmailField(unique=True)
    institucion = models.CharField(max_length=100, null=True, blank=True)
    rol = models.CharField(max_length=20, default='estudiante')
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # CAMPOS CLAVE
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    objects = UsersManager()

    def __str__(self):
        return self.nombre

    # PERMISOS
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True