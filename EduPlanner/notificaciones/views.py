from django.views.generic import ListView
from .models import Notificacion
from django.contrib.auth.mixins import LoginRequiredMixin

class ListaNotificacionesView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'notificaciones/notificaciones_lista.html'
    context_object_name = 'notificaciones'

    def get_queryset(self):
        return self.model.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
