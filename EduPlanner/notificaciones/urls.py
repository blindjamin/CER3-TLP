from django.urls import path
from .views import ListaNotificacionesView

urlpatterns = [
    path('', ListaNotificacionesView.as_view(), name='notificaciones_lista'),
]
