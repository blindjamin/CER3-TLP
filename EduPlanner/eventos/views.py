from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .models import Evento
from feriados.models import Feriado  
from .forms import EventoForm
from django.contrib import messages
from django.utils.safestring import mark_safe

# Mixin para verificar si el usuario es administrador
def es_administrador(usuario):
    return usuario.is_authenticated and usuario.role == 'admin'

class AdministradorRequeridoMixin:
    @method_decorator(login_required)
    @method_decorator(user_passes_test(es_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# Vista para listar eventos
class ListaEventosView(ListView):
    model = Evento
    template_name = 'eventos/eventos_lista.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        """
        Filtra los eventos según el tipo de evento si se pasa el parámetro `tipo`.
        Si no hay parámetro, muestra todos los eventos.
        """
        queryset = super().get_queryset()
        tipo = self.request.GET.get('tipo')  # Obtiene el tipo desde la URL (query params)
        if tipo:
            queryset = queryset.filter(type=tipo)  # Filtra por tipo
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto, como la lista de tipos disponibles.
        """
        context = super().get_context_data(**kwargs)
        context['tipos_eventos'] = [
            ('inicio_semestre', 'Inicio de Semestre'),
            ('fin_semestre', 'Fin de Semestre'),
            ('inicio_inscripcion', 'Inicio de Inscripción de Asignaturas'),
            ('fin_inscripcion', 'Fin de Inscripción de Asignaturas'),
            ('receso', 'Receso Académico'),
            ('feriado_nacional', 'Feriado Nacional'),
            ('feriado_regional', 'Feriado Regional'),
            ('inicio_solicitudes', 'Inicio de Plazos de Solicitudes Administrativas'),
            ('fin_solicitudes', 'Fin de Plazos de Solicitudes Administrativas'),
            ('inicio_beneficios', 'Inicio de Plazos para la Gestión de Beneficios'),
            ('fin_beneficios', 'Fin de Plazos para la Gestión de Beneficios'),
            ('ceremonia_titulacion', 'Ceremonia de Titulación o Graduación'),
            ('reunion_consejo', 'Reunión de Consejo Académico'),
            ('taller_charla', 'Talleres y Charlas'),
            ('orientacion', 'Día de Orientación para Nuevos Estudiantes'),
            ('extracurricular', 'Eventos Extracurriculares'),
            ('inicio_clases', 'Inicio de Clases'),
            ('ultimo_dia_clases', 'Último Día de Clases'),
            ('puertas_abiertas', 'Día de Puertas Abiertas'),
            ('suspension_completa', 'Suspensión de Actividades Completa'),
            ('suspension_parcial', 'Suspensión de Actividades Parcial'),
        ]
        return context


# Vista para crear un evento
class CrearEventoView(AdministradorRequeridoMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_formulario.html'
    success_url = reverse_lazy('eventos_lista')

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Asigna el usuario actual como creador
        return super().form_valid(form)

# Vista para actualizar un evento
class ActualizarEventoView(AdministradorRequeridoMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_formulario.html'
    success_url = reverse_lazy('eventos_lista')

# Vista para ver el detalle de un evento
class DetalleEventoView(DetailView):
    model = Evento
    template_name = 'eventos/evento_detalle.html'
    context_object_name = 'evento'

# Vista para eliminar un evento
class EliminarEventoView(AdministradorRequeridoMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirmar_eliminacion.html'
    success_url = reverse_lazy('eventos_lista')

class VistaCalendarioConsolidado(TemplateView):
    template_name = 'eventos/calendario_consolidado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eventos = Evento.objects.all()
        feriados = Feriado.objects.all()

        # Procesar eventos y feriados para prepararlos para el calendario
        calendario = []
        for evento in eventos:
            calendario.append({
                "title": evento.title,
                "start": evento.start_date,
                "end": evento.end_date,
                "color": getattr(evento, "color", "#3788d8"),  # Color predeterminado si no hay atributo 'color'
            })
        for feriado in feriados:
            calendario.append({
                "title": feriado.name,
                "start": feriado.date,
                "end": feriado.date,  # Los feriados tienen la misma fecha de inicio y fin
                "color": "#FF0000",  # Color específico para feriados
            })

        # Agregar datos procesados al contexto
        context['calendario'] = calendario
        return context