from django.core.paginator import Paginator
from django.shortcuts import render
from .models import EventoCultural

def evento_cultural_view(request):
    eventos = EventoCultural.objects.filter(publicado=True).order_by('fecha_inicio')
    paginator = Paginator(eventos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eventos/evento_cultural_list.html', {'page_obj': page_obj})