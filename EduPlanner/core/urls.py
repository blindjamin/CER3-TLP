from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('usuarios/', include('usuarios.urls')), 
    path('eventos/', include('eventos.urls')),  
    path('feriados/', include('feriados.urls')),  
    path('api/', include('api.urls')), 
    path('notificaciones/', include('notificaciones.urls')),
]
