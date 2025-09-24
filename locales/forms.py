from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Relato, SugerenciaNegocio, Receta, PerfilUsuario, ReclamoNegocio


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username']

# Este es el formulario original, lo mantendremos para uso exclusivo del admin
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['biografia', 'telefono', 'ubicacion', 'avatar', 'rango']

# Este es el nuevo formulario para los usuarios normales
class PerfilUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['biografia', 'telefono', 'ubicacion', 'avatar']

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
<<<<<<< HEAD
        )


class ReclamoNegocioForm(forms.ModelForm):
    class Meta:
        model = ReclamoNegocio
        fields = ['negocio', 'contrato_pdf', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe tu relación con el negocio...'}),
        }
=======
        )
>>>>>>> b6775cbd93cb0536cf694a786638a2e195f9f614
