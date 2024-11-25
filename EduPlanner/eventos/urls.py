from django.urls import path
from .views import (
    ListaEventosView, CrearEventoView, ActualizarEventoView,
    DetalleEventoView, EliminarEventoView, VistaCalendarioConsolidado, calendario_view
)

urlpatterns = [
    path('', ListaEventosView.as_view(), name='eventos_lista'),
    path('crear/', CrearEventoView.as_view(), name='evento_crear'),
    path('<int:pk>/', DetalleEventoView.as_view(), name='evento_detalle'),
    path('<int:pk>/editar/', ActualizarEventoView.as_view(), name='evento_editar'),
    path('<int:pk>/eliminar/', EliminarEventoView.as_view(), name='evento_eliminar'),
    #path('calendario/', VistaCalendarioConsolidado.as_view(), name='calendario_consolidado'),
    path('calendario/', calendario_view, name='calendario_bootstrap'),
]
