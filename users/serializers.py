from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
   
class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField()