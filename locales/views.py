from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms import ModelForm  # ✅ Importación correcta

from .forms import (
    RecetaForm,
    PerfilUsuarioForm,
    UserRegisterForm,
    UserLoginForm,
    RelatoForm,
    SugerenciaNegocioForm
)
from .models import (
    Receta,
    PerfilUsuario,
    Relato,
    Negocio,
    SaberPopular
)
from eventos.models import EventoCultural
from django.utils.http import urlencode


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
                PerfilUsuario.objects.get_or_create(usuario=user)
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

    perfil = None
    if request.user.is_authenticated:
        perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)

    context = {
        'relatos': relatos,
        'negocios': negocios,
        'perfil': perfil,
    }
    return render(request, 'locales/home.html', context)


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
    map_url = f"https://maps.google.com/maps?q=?q={ubicacion}&output=embed"
    html = render_to_string('locales/mapa_fragmento.html', {'map_url': map_url})
    return HttpResponse(html)


@login_required
def create_receta_view(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.estado = 'pending'
            receta.save()
            messages.success(request, 'Receta enviada para revisión. ¡Gracias por compartir tu conocimiento!')
            return redirect('biblioteca_view')
    else:
        form = RecetaForm()
    return render(request, 'locales/create_receta.html', {'form': form})


def biblioteca_view(request):
    query = request.GET.get('q')
    recetas_list = Receta.objects.filter(estado='approved')
    saberes_list = SaberPopular.objects.filter(estado='approved')

    if query:
        recetas_list = recetas_list.filter(
            Q(titulo__icontains=query) | Q(ingredientes__icontains=query) | Q(pasos__icontains=query)
        )
        saberes_list = saberes_list.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )

    recetas_paginator = Paginator(recetas_list, 10)
    saberes_paginator = Paginator(saberes_list, 10)

    recetas = recetas_paginator.get_page(request.GET.get('page_recetas'))
    saberes = saberes_paginator.get_page(request.GET.get('page_saberes'))

    context = {
        'recetas': recetas,
        'saberes': saberes,
        'query': query,
    }
    return render(request, 'locales/biblioteca.html', context)


def evento_cultural_list(request):
    eventos_list = EventoCultural.objects.all().order_by('fecha_inicio')
    paginator = Paginator(eventos_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'eventos/evento_cultural_list.html', {'page_obj': page_obj})


@login_required
def editar_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil_view')
    else:
        form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})


@login_required
def eliminar_avatar(request):
    perfil = request.user.perfilusuario
    perfil.avatar.delete(save=True)
    messages.success(request, 'Tu imagen de perfil ha sido eliminada.')
    return redirect('perfil_view')


@login_required
def lista_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related('usuario').all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def perfil_publico(request, username):
    perfil = get_object_or_404(PerfilUsuario, usuario__username=username)
    return render(request, 'usuarios/perfil_publico.html', {'perfil': perfil})


class RangoForm(ModelForm):  # ✅ Usamos ModelForm directamente
    class Meta:
        model = PerfilUsuario
        fields = ['rango']


