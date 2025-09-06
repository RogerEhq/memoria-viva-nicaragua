from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Relato, SugerenciaNegocio

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username']

# Nuevo formulario para los relatos
class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relato
        fields = ['title', 'content', 'image']

# Nuevo formulario para las sugerencias de negocios
class SugerenciaNegocioForm(forms.ModelForm):
    class Meta:
        model = SugerenciaNegocio
        fields = ['nombre_negocio', 'ubicacion_texto', 'comentarios']