from django.urls import path
from .views import registro,CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registro/', registro, name='registro'),  # Tu vista de registro existente
    path('login/', CustomLoginView.as_view(template_name='usuarios/login.html'), name='login'),  # Nueva vista personalizada
    path('logout/', LogoutView.as_view(), name='logout'),
]