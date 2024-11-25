from django.shortcuts import render

from django.shortcuts import render
from .models import Feriado

def lista_feriados(request):
    feriados = Feriado.objects.all() 
    return render(request, 'feriados/feriados_lista.html', {'feriados': feriados})
