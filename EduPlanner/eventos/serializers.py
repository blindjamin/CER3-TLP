from rest_framework import serializers
from .models import Evento,Revision

class EventoSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Evento
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'type', 'type_display', 'status', 'is_official', 'created_by']
        read_only_fields = ['id', 'created_by', 'type_display']

class RevisionSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True)

    class Meta:
        model = Revision
        fields = ['id', 'event', 'event_title', 'reviewed_by', 'reviewed_by_username', 'comments', 'status', 'reviewed_at']
        read_only_fields = ['id', 'reviewed_at', 'event_title', 'reviewed_by_username']
