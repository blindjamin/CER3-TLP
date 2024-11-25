from django.urls import path
from .views import lista_feriados

urlpatterns = [
    path('', lista_feriados, name='feriados_lista'),
]
