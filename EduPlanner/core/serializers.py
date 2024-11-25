from rest_framework import serializers
from eventos.models import Evento
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Notificacion
        fields = ['id', 'event', 'event_title', 'message', 'created_at']
        read_only_fields = ['id', 'created_at', 'event_title']
