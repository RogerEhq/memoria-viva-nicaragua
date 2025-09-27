from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Relato, SugerenciaNegocio, Receta, PerfilUsuario, ReclamoNegocio

# Registro de usuario
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Registrarse')
        )

# Inicio de sesión
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Iniciar sesión')
        )

# Perfil de usuario (creación)
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['biografia', 'telefono', 'ubicacion', 'avatar', 'rango']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'biografia',
            'telefono',
            'ubicacion',
            'avatar',
            'rango',
            Submit('submit', 'Guardar perfil')
        )

# Perfil de usuario (actualización)
class PerfilUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['biografia', 'telefono', 'ubicacion', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'biografia',
            'telefono',
            'ubicacion',
            'avatar',
            Submit('submit', 'Actualizar perfil')
        )

# Formulario de relatos
class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relato
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            'image',
            Submit('submit', 'Enviar relato')
        )

# Formulario de sugerencia de negocio
class SugerenciaNegocioForm(forms.ModelForm):
    # Campos ocultos para latitud y longitud
    latitud = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitud = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SugerenciaNegocio
        # Incluir latitud y longitud en los campos del formulario
        fields = ['nombre_negocio', 'ubicacion_texto', 'latitud', 'longitud', 'comentarios', 'categoria_negocio',
                  'foto_referencia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_negocio'].label = "Categoría del negocio"
        self.fields['categoria_negocio'].empty_label = None

        # Ocultar campos en el layout de crispy-forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre_negocio',
            'ubicacion_texto',
            'comentarios',
            'categoria_negocio',
            'foto_referencia',
            # Añadir los campos ocultos al layout
            'latitud',
            'longitud',
            Submit('submit', 'Enviar sugerencia')
        )

# Formulario de recetas
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
            Submit('submit', 'Enviar receta')
        )

# Formulario de reclamo de negocio
class ReclamoNegocioForm(forms.ModelForm):
    class Meta:
        model = ReclamoNegocio
        fields = ['negocio', 'contrato_pdf', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe tu relación con el negocio...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'negocio',
            'contrato_pdf',
            'mensaje',
            Submit('submit', 'Enviar reclamo')
        )
