from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Página de inicio
    path('usuarios/', include('usuarios.urls')),  # URLs de usuarios
    path('eventos/', include('eventos.urls')),  # URLs de eventos
    path('feriados/', include('feriados.urls')),  # URLs de feriados
    path('api/', include('api.urls')),  # URLs de API
    path('notificaciones/', include('notificaciones.urls')),
]
