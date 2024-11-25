from rest_framework import serializers
from .models import Feriado

class FeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = ['id', 'name', 'date', 'region']
        read_only_fields = ['id']
