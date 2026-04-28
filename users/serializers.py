from rest_framework import serializers
from .models import Users
import re

from rest_framework import serializers
from .models import Users
import re


class UsersSerializer(serializers.ModelSerializer):

    foto_url = serializers.SerializerMethodField()
    foto = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Users
        fields = [
            'id',
            'nombre',
            'correo',
            'password',
            'rol',
            'estado',
            'fecha_nacimiento',
            'identificacion',
            'institucion',
            'foto',
            'foto_url', 
            'last_login',
        ]

        extra_kwargs = {
            'password': {'write_only': True}, 
            'rol': {'read_only': True},
            'last_login': {'read_only': True},
        }


    def get_foto_url(self, obj):
        if obj.foto:
            return obj.foto.url
        
        return "https://res.cloudinary.com/dyirgkxjq/image/upload/v1/default_avatar.png"


    # =====================================================
    # VALIDAR CORREO
    # =====================================================
    def validate_correo(self, value):
        value = value.lower()
        qs = Users.objects.filter(correo=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("El correo ya existe")
        return value

    # =====================================================
    # VALIDAR PASSWORD
    # =====================================================
    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener mínimo 8 caracteres."
            )

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Debe contener al menos una mayúscula."
            )

        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "Debe contener al menos un número."
            )

        return value

    # =====================================================
    # CREATE
    # =====================================================
    def create(self, validated_data):

        password = validated_data.pop('password')

        user = Users(**validated_data)
        user.set_password(password)
        user.save()

        return user

    # =====================================================
    # UPDATE
    # =====================================================
    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =========================================================
# LOGIN
# =========================================================
class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField()