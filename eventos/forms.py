from django import forms
from .models import EventoCultural

class EventoCulturalForm(forms.ModelForm):
    class Meta:
        model = EventoCultural
        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'ubicacion_texto',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del evento'
            }),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'ubicacion_texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación del evento'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(EventoCulturalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # Asegura que todos los campos sean obligatorios