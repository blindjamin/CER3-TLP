from django.urls import path
from .views import registro,CustomLoginView, CambiarRolView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registro/', registro, name='registro'),  
    path('login/', CustomLoginView.as_view(template_name='usuarios/login.html'), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/cambiar-rol/', CambiarRolView.as_view(), name='cambiar_rol'),
]
