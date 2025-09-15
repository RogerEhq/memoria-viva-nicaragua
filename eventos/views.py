from django.shortcuts import render
from .models import EventoCultural

def evento_cultural_list(request):
    eventos = EventoCultural.objects.all().order_by('fecha_inicio')
    return render(request, 'eventos/evento_cultural_list.html', {'eventos': eventos})

# Create your views here.
