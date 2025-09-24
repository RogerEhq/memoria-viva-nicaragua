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
from django.db.models import Avg

from django.forms import ModelForm


from .forms import (
    RecetaForm,
    # 💡 Importa el nuevo formulario
    PerfilUsuarioUpdateForm,
    UserRegisterForm,
    UserLoginForm,
    RelatoForm,
    SugerenciaNegocioForm,
    ReclamoNegocioForm

)
from .models import (
    Receta,
    PerfilUsuario,
    Relato,
    Negocio,
    SaberPopular, Comentario, Calificacion, ReporteComentario,ReclamoNegocio
)
from eventos.models import EventoCultural
from django.utils.http import urlencode


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 💡 Creamos el PerfilUsuario al registrarse para evitar errores
            PerfilUsuario.objects.get_or_create(usuario=user)
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
                # 💡 Aseguramos que el perfil existe al iniciar sesión
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
def perfil_view(request):
    # 💡 Perfil del usuario autenticado
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    return render(request, 'usuarios/perfil_view.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        # 💡 Usamos el nuevo formulario sin el campo 'rango'
        form = PerfilUsuarioUpdateForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('perfil_view')
    else:
        # 💡 Usamos el nuevo formulario sin el campo 'rango'
        form = PerfilUsuarioUpdateForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'perfil': perfil})


@login_required
def eliminar_avatar(request):
    perfil = request.user.perfilusuario
    if perfil.avatar:
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


class RangoForm(ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rango']

@login_required

def reclamar_negocio(request):
    negocio_id = request.GET.get('negocio_id')
    negocio = get_object_or_404(Negocio, id=negocio_id) if negocio_id else None

    if request.method == 'POST':
        form = ReclamoNegocioForm(request.POST, request.FILES)
        if form.is_valid():
            reclamo = form.save(commit=False)
            reclamo.usuario = request.user
            reclamo.save()
            messages.success(request, "Su solicitud de reclamo será examinada.")
            return redirect('home_view')
    else:
        form = ReclamoNegocioForm(initial={'negocio': negocio})

    return render(request, 'locales/reclamar_negocio.html', {
        'form': form,
        'negocio': negocio
    })

def detalle_negocio(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)

    comentarios = Comentario.objects.filter(negocio=negocio).select_related('usuario')
    for comentario in comentarios:
        calificacion = Calificacion.objects.filter(comentario=comentario).first()
        comentario.puntuacion_usuario = calificacion.puntuacion if calificacion else None

    calificaciones = Calificacion.objects.filter(negocio=negocio)
    promedio = calificaciones.aggregate(promedio=Avg('puntuacion'))['promedio'] or 0

    user_calificacion = None
    if request.user.is_authenticated:
        user_calificacion = Calificacion.objects.filter(negocio=negocio, usuario=request.user).first()

    return render(request, 'locales/detalle_negocio.html', {
        'negocio': negocio,
        'comentarios': comentarios,
        'calificaciones': calificaciones,
        'promedio': round(promedio, 1),
        'user_calificacion': user_calificacion,
    })



def lista_negocios(request):
    departamento = request.GET.get('departamento')
    if departamento:
        negocios = Negocio.objects.filter(address_text__icontains=departamento)
    else:
        negocios = Negocio.objects.all()

    departamentos = Negocio.objects.values_list('address_text', flat=True).distinct()
    return render(request, 'locales/lista_negocios.html', {
        'negocios': negocios,
        'departamentos': departamentos
    })

@login_required
def reportar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        if motivo:
            ReporteComentario.objects.create(
                comentario=comentario,
                usuario=request.user,
                motivo=motivo
            )
            messages.success(request, "Tu reporte llego a nuestros moderadores.")
        return redirect('detalle_negocio', negocio_id=comentario.negocio.id)
    return render(request, 'locales/reportar_comentario.html', {'comentario': comentario})

def juego_view(request):
    return render(request, 'locales/juego.html')

@login_required
def agregar_comentario(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(
                negocio=negocio,
                usuario=request.user,
                texto=texto
            )
            messages.success(request, "Comentario enviado correctamente.")
    return redirect('detalle_negocio', negocio_id=negocio.id)

@login_required
def agregar_calificacion(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if request.method == 'POST':
        puntuacion = request.POST.get('puntuacion')
        if puntuacion:
            Calificacion.objects.create(
                negocio=negocio,
                usuario=request.user,
                puntuacion=int(puntuacion)
            )
            messages.success(request, "Calificación registrada correctamente.")
    return redirect('detalle_negocio', negocio_id=negocio.id)

def juego_view(request):
    return render(request, 'locales/juego.html')

@login_required
def comentar_y_calificar(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if request.method == 'POST':
        texto = request.POST.get('texto')
        puntuacion = request.POST.get('puntuacion')

        if texto and puntuacion:
            comentario = Comentario.objects.create(
                negocio=negocio,
                usuario=request.user,
                texto=texto
            )
            Calificacion.objects.create(
                negocio=negocio,
                usuario=request.user,
                comentario=comentario,
                puntuacion=int(puntuacion)
            )
            messages.success(request, "Tu comentario y calificación fueron enviados.")
        else:
            messages.error(request, "Debes completar ambos campos.")
    return redirect('detalle_negocio', negocio_id=negocio.id)
