from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator

from eventos.models import EventoCultural
from .forms import UserRegisterForm, UserLoginForm, RelatoForm, SugerenciaNegocioForm
from .models import Relato, Negocio, Receta, SaberPopular


# Vistas existentes...

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login_view')
    else:
        form = UserRegisterForm()
    return render(request, 'locales/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}!')
                return redirect('home_view')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = UserLoginForm()
    return render(request, 'locales/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('login_view')


def home_view(request):
    relatos = Relato.objects.filter(status='approved')
    negocios = Negocio.objects.all()
    return render(request, 'locales/home.html', {'relatos': relatos, 'negocios': negocios})


@login_required
def create_relato_view(request):
    if request.method == 'POST':
        form = RelatoForm(request.POST, request.FILES)
        if form.is_valid():
            relato = form.save(commit=False)
            relato.author = request.user
            relato.save()
            messages.success(request, 'Relato enviado para revisión. ¡Gracias por tu contribución!')
            return redirect('home_view')
    else:
        form = RelatoForm()
    return render(request, 'locales/create_relato.html', {'form': form})


@login_required
def sugerir_negocio_view(request):
    if request.method == 'POST':
        form = SugerenciaNegocioForm(request.POST)
        if form.is_valid():
            sugerencia = form.save(commit=False)
            sugerencia.sugerido_por = request.user
            sugerencia.save()
            messages.success(request, '¡Sugerencia enviada! El equipo la revisará pronto.')
            return redirect('home_view')
    else:
        form = SugerenciaNegocioForm()
    return render(request, 'locales/sugerir_negocio.html', {'form': form})


def mostrar_mapa(request):
    ubicacion = request.GET.get('ubicacion', '')
    html = render_to_string('locales/mapa_fragmento.html', {'ubicacion': ubicacion})
    return HttpResponse(html)


# 📚 Nueva vista para la Biblioteca de Saberes
def biblioteca_view(request):
    query = request.GET.get('q')

    recetas_list = Receta.objects.filter(estado='approved')
    saberes_list = SaberPopular.objects.filter(estado='approved')

    if query:
        # Búsqueda usando Q objects en ambos modelos
        recetas_list = recetas_list.filter(
            Q(titulo__icontains=query) | Q(ingredientes__icontains=query) | Q(pasos__icontains=query)
        )
        saberes_list = saberes_list.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )

    # Paginación para los resultados de la biblioteca
    recetas_paginator = Paginator(recetas_list, 10)  # Muestra 10 recetas por página
    saberes_paginator = Paginator(saberes_list, 10)  # Muestra 10 saberes por página

    recetas_page_number = request.GET.get('page_recetas')
    saberes_page_number = request.GET.get('page_saberes')

    recetas = recetas_paginator.get_page(recetas_page_number)
    saberes = saberes_paginator.get_page(saberes_page_number)

    context = {
        'recetas': recetas,
        'saberes': saberes,
        'query': query,
    }
    return render(request, 'locales/biblioteca.html', context)


# 🗓️ Nueva vista para la app de eventos
def evento_cultural_list(request):
    eventos_list = EventoCultural.objects.all().order_by('fecha_inicio')

    # Paginación para eventos
    paginator = Paginator(eventos_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'eventos/evento_cultural_list.html', {'page_obj': page_obj})