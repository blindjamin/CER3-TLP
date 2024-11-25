from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import User
from .forms import RegistroForm, CustomAuthenticationForm
from .serializers import UserSerializer
from django.contrib.auth.views import LoginView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    
# Vista para registrar usuarios
@csrf_protect
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
        else:
            return render(request, 'usuarios/registro.html', {'form': form, 'errors': form.errors})
    form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# Vista para iniciar sesión
@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'usuarios/login.html')

# Vista para cerrar sesión
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('login')


@user_passes_test(lambda user: getattr(user, 'role', None) == 'admin')
def gestion_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/gestion_usuarios.html', {'usuarios': usuarios})


# API para listar usuarios
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        users = User.objects.all()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# Decorador para verificar si es superadmin
def es_superadmin(usuario):
    return usuario.is_authenticated and usuario.is_superuser

@method_decorator([login_required, user_passes_test(es_superadmin)], name='dispatch')
class CambiarRolView(UpdateView):
    model = User
    fields = ['role']
    template_name = 'usuarios/cambiar_rol.html'
    success_url = reverse_lazy('lista_usuarios')  

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)