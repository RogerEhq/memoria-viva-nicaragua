from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, RelatoForm, SugerenciaNegocioForm
from .models import Relato, Negocio, SugerenciaNegocio

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