from django.urls import path
from .views import EventoListCreateAPIView, FeriadoListAPIView, NotificacionListAPIView, CalendarioConsolidadoAPIView

urlpatterns = [
    path('eventos/', EventoListCreateAPIView.as_view(), name='eventos'),
    path('feriados/', FeriadoListAPIView.as_view(), name='feriados'),
    path('notificaciones/', NotificacionListAPIView.as_view(), name='notificaciones'),
    path('calendario/', CalendarioConsolidadoAPIView.as_view(), name='calendario'),
]
