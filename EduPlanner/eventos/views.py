from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render
from .models import Evento
from feriados.models import Feriado
from .forms import EventoForm
from django.contrib import admin


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
        tipo = self.request.GET.get('tipo')  # Filtra por tipo si se proporciona
        queryset = super().get_queryset()
        if tipo:
            queryset = queryset.filter(type=tipo)
        return queryset

    def get_context_data(self, **kwargs):
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
        form.instance.created_by = self.request.user
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


# Vista para el calendario consolidado
class VistaCalendarioConsolidado(TemplateView):
    template_name = 'eventos/calendario_bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eventos = Evento.objects.all()
        feriados = Feriado.objects.all()

        calendario = [
            {"title": evento.title, "start": evento.start_date, "end": evento.end_date, "color": getattr(evento, "color", "#3788d8")}
            for evento in eventos
        ] + [
            {"title": feriado.name, "start": feriado.date, "end": feriado.date, "color": "#FF0000"}
            for feriado in feriados
        ]

        context['calendario'] = calendario
        return context


# Registrar Evento en el admin
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'description')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')


# Vista para el calendario con Bootstrap
def calendario_view(request):
    fecha_seleccionada = request.GET.get('date')
    eventos = Evento.objects.filter(start_date__lte=fecha_seleccionada, end_date__gte=fecha_seleccionada) if fecha_seleccionada else Evento.objects.all()
    return render(request, 'eventos/calendario_bootstrap.html', {'eventos': eventos})
