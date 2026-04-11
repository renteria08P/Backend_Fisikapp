from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password

class UsersSerializer(serializers.ModelSerializer):
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
            'institucion'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = Users(**validated_data)
        user.set_password(password) 
        user.save()
        
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password) 

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField()