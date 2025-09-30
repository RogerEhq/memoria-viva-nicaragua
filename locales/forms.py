from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Relato, SugerenciaNegocio, Receta, PerfilUsuario, ReclamoNegocio, Negocio, MensajePropietario, \
    Comentario, Calificacion


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
    latitud = forms.DecimalField(max_digits=20, decimal_places=15, required=False, widget=forms.HiddenInput())
    longitud = forms.DecimalField(max_digits=20, decimal_places=15, required=False, widget=forms.HiddenInput())
    ubicacion_texto = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Relato
        fields = ['title', 'content', 'image', 'latitud', 'longitud', 'ubicacion_texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            'image',
            'ubicacion_texto',
            'latitud',
            'longitud',
            Submit('submit', 'Enviar relato')
        )


# Formulario de sugerencia de negocio (CORREGIDO)
class SugerenciaNegocioForm(forms.ModelForm):
    # Campos ocultos para latitud y longitud. Ahora se definen aquí
    latitud = forms.DecimalField(max_digits=20, decimal_places=15, required=False, widget=forms.HiddenInput())
    longitud = forms.DecimalField(max_digits=20, decimal_places=15, required=False, widget=forms.HiddenInput())

    # Campo de categoría (obligatorio por defecto)
    categoria_relacionada = forms.ModelChoiceField(
        queryset=SugerenciaNegocio.categoria_relacionada.field.related_model.objects.all(),
        label="Categoría Relacionada",
        required=True  # El campo vuelve a ser obligatorio
    )

    class Meta:
        model = SugerenciaNegocio
        fields = ['nombre_negocio', 'ubicacion_texto', 'latitud', 'longitud',
                  'comentarios', 'categoria_relacionada', 'foto_referencia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comentarios'].required = False
        self.fields['foto_referencia'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre_negocio',
            'ubicacion_texto',
            'comentarios',
            'categoria_relacionada',
            'foto_referencia',
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


# NUEVO: Formulario para el propietario del negocio
class NegocioPaquetesForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['paquetes_turismo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('paquetes_turismo', css_class='form-control-lg'),
            Submit('submit', 'Guardar Paquetes de Turismo', css_class='btn btn-primary mt-3')
        )


# NUEVO: Formulario para la edición general del negocio
# En tu archivo forms.py, en la línea 197 o similar.

class NegocioForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = [
            'name',
            'description',
            'address_text',
            'phone',
            'email',
            'website',
            'categoria_relacionada',
            'is_turismo',
            'foto_principal'  # <-- Asegúrate de que este nombre sea correcto
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            'address_text',
            'phone',
            'email',
            'website',
            'categoria_relacionada',
            'is_turismo',
            'foto_principal',  # <-- Asegúrate de que este nombre sea correcto
            Submit('submit', 'Guardar Cambios')
        )


# NUEVO: Formulario para que el propietario envíe un mensaje al admin
class MensajePropietarioForm(forms.ModelForm):
    class Meta:
        model = MensajePropietario
        fields = ['asunto', 'cuerpo']
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe tu problema o sugerencia.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'asunto',
            'cuerpo',
            Submit('submit', 'Enviar Mensaje')
        )


# NUEVO: Formulario para el comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario aquí...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'texto',
            Submit('submit', 'Enviar Comentario')
        )


# NUEVO: Formulario para la calificación
class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['puntuacion']
        widgets = {
            'puntuacion': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'puntuacion',
            Submit('submit', 'Enviar Calificación')
        )