from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Relato, SugerenciaNegocio, Receta

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username']

class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relato
        fields = ['title', 'content', 'image']

class SugerenciaNegocioForm(forms.ModelForm):
    class Meta:
        model = SugerenciaNegocio
        fields = ['nombre_negocio', 'ubicacion_texto', 'comentarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre_negocio',
            'ubicacion_texto',
            'comentarios',
            Submit('submit', 'Enviar Sugerencia')
        )

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'ingredientes', 'pasos', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'titulo',
            'descripcion',
            'ingredientes',
            'pasos',
            'imagen',
            Submit('submit', 'Enviar Receta')
        )