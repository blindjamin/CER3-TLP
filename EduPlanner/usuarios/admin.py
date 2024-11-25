from django.contrib import admin
from .models import User
from eventos.models import Evento

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

class EventoAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'start_date', 'end_date', 'created_by')
    list_filter = ('type', 'status')
    search_fields = ('title',)
