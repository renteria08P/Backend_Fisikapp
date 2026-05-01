from rest_framework import serializers
from .models import Log, Notificacion


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha'] 

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_creacion'] 