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
from django.forms import ModelForm
from django.db.models import Avg
from django.db import IntegrityError # <-- LÍNEA CORREGIDA
from django.utils import timezone # Se importa timezone para uso en funciones

# Importaciones necesarias para el filtro de categorías
from .models import Negocio, Categoria, PerfilUsuario, Relato, SaberPopular, Comentario, Calificacion, \
    ReporteComentario, ReclamoNegocio, SugerenciaNegocio, Receta, MensajePropietario
from .forms import (
    RecetaForm,
    PerfilUsuarioUpdateForm,
    UserRegisterForm,
    UserLoginForm,
    RelatoForm,
    SugerenciaNegocioForm,
    ReclamoNegocioForm,
    NegocioPaquetesForm,
    NegocioForm,
    MensajePropietarioForm,
    ComentarioForm,
    CalificacionForm
)
from eventos.models import EventoCultural
from django.utils.http import urlencode


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Creamos el PerfilUsuario al registrarse para evitar errores
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
                # Aseguramos que el perfil existe al iniciar sesión
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
    # Obtener negocios, calcular la calificación promedio y ordenarlos de mayor a menor
    negocios = Negocio.objects.annotate(
        avg_rating=Avg('calificacion__puntuacion')
    ).order_by('-avg_rating')
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
        form = SugerenciaNegocioForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                sugerencia = form.save(commit=False)
                sugerencia.sugerido_por = request.user
                sugerencia.save()
                messages.success(request, '¡Sugerencia enviada! El equipo la revisará pronto.')
                return redirect('sugerir_negocio_view')
            except Exception as e:
                print("Error inesperado al guardar la sugerencia:")
                print(e)
                messages.error(request, f'Ocurrió un error inesperado al enviar la sugerencia: {e}.')
        else:
            print("El formulario no es válido. Errores:")
            print(form.errors)
            messages.error(request, 'Hubo un error al enviar la sugerencia. Revisa los campos.')
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
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    return render(request, 'usuarios/perfil_view.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = PerfilUsuarioUpdateForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('perfil_view')
    else:
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

    # Agrega esto para calcular la calificación promedio
    promedio = negocio.calificacion_set.aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0

    # Pasa los formularios vacíos al contexto
    comentario_form = ComentarioForm()
    calificacion_form = CalificacionForm()

    context = {
        'negocio': negocio,
        'comentarios': comentarios,
        'promedio': round(promedio, 1),
        'comentario_form': comentario_form, # <-- Agregado
        'calificacion_form': calificacion_form, # <-- Agregado
        'is_turismo_negocio': negocio.is_turismo,
    }
    return render(request, 'locales/detalle_negocio.html', context)


def detalle_paquetes_turismo(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if not negocio.is_turismo or not negocio.paquetes_turismo:
        messages.error(request, "Este negocio no tiene paquetes de turismo o no pertenece a esa categoría.")
        return redirect('detalle_negocio', negocio_id=negocio.id)
    context = {
        'negocio': negocio,
    }
    return render(request, 'locales/detalle_paquetes_turismo.html', context)


def plan_turismo(request):
    negocios_turismo = Negocio.objects.filter(categoria_relacionada__slug='turismo')
    context = {
        'negocios': negocios_turismo,
    }
    return render(request, 'locales/plan_turismo.html', context)


def lista_negocios(request):
    categoria_slug = request.GET.get('categoria', None)
    departamento_seleccionado = request.GET.get('departamento', None)
    if categoria_slug == 'turismo':
        return redirect('plan_turismo')
    negocios = Negocio.objects.all()
    categorias = Categoria.objects.all()
    if categoria_slug:
        negocios = negocios.filter(categoria_relacionada__slug=categoria_slug)
    if departamento_seleccionado:
        negocios = negocios.filter(address_text__icontains=departamento_seleccionado)
    departamentos_unicos = set()
    for negocio in Negocio.objects.all():
        if negocio.address_text:
            partes = negocio.address_text.split(',')
            if len(partes) > 0:
                departamentos_unicos.add(partes[0].strip())
    contexto = {
        'negocios': negocios,
        'categorias': categorias,
        'departamentos': sorted(list(departamentos_unicos)),
        'departamento_actual': departamento_seleccionado,
        'categoria_actual_slug': categoria_slug,
    }
    return render(request, 'locales/lista_negocios.html', contexto)


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
def comentar_y_calificar(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        calificacion_form = CalificacionForm(request.POST)
        if comentario_form.is_valid() and calificacion_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.negocio = negocio
            comentario.usuario = request.user
            comentario.save()
            calificacion = calificacion_form.save(commit=False)
            calificacion.negocio = negocio
            calificacion.usuario = request.user
            calificacion.comentario = comentario
            calificacion.save()
            messages.success(request, '¡Gracias por tu comentario y calificación!')
        else:
            messages.error(request, 'Hubo un problema con tu comentario o calificación. Por favor, revisa los campos.')
        return redirect('detalle_negocio', negocio_id=negocio.id)
    else:
        comentario_form = ComentarioForm()
        calificacion_form = CalificacionForm()
    context = {
        'negocio': negocio,
        'comentario_form': comentario_form,
        'calificacion_form': calificacion_form,
    }
    return render(request, 'locales/comentar_y_calificar.html', context)


@staff_member_required
def aprobar_foto_referencia_view(request, sugerencia_id):
    sugerencia = get_object_or_404(SugerenciaNegocio, id=sugerencia_id)
    sugerencia.foto_aprobada = True
    sugerencia.save()
    negocio = Negocio.objects.filter(name=sugerencia.nombre_negocio).first()
    if negocio:
        negocio.foto_principal = sugerencia.foto_referencia
        negocio.save()
    messages.success(request, "Foto aprobada y vinculada al negocio.")
    return redirect('/admin/')


@login_required
def editar_paquetes_turismo(request, negocio_id):
    negocio = get_object_or_404(Negocio, id=negocio_id)
    if request.user != negocio.propietario:
        messages.error(request, "No tienes permiso para editar este negocio.")
        return redirect('detalle_negocio', negocio_id=negocio.id)
    if request.method == 'POST':
        form = NegocioPaquetesForm(request.POST, instance=negocio)
        if form.is_valid():
            form.save()
            messages.success(request, "Los paquetes de turismo se han actualizado correctamente.")
            return redirect('detalle_negocio', negocio_id=negocio.id)
    else:
        form = NegocioPaquetesForm(instance=negocio)
    context = {
        'form': form,
        'negocio': negocio,
    }
    return render(request, 'locales/editar_paquetes.html', context)


@login_required
def editar_negocio(request, pk):
    negocio = get_object_or_404(Negocio, pk=pk)
    if request.user != negocio.propietario:
        messages.error(request, "No tienes permiso para editar este negocio.")
        return redirect('detalle_negocio', negocio_id=negocio.pk)
    if request.method == 'POST':
        form = NegocioForm(request.POST, request.FILES, instance=negocio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Los cambios se han guardado exitosamente!')
            return redirect('detalle_negocio', negocio_id=negocio.pk)
    else:
        form = NegocioForm(instance=negocio)
    context = {
        'form': form,
        'negocio': negocio,
    }
    return render(request, 'locales/editar_negocio.html', context)


@login_required
def enviar_mensaje_admin(request):
    if request.method == 'POST':
        form = MensajePropietarioForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.propietario = request.user
            mensaje.save()
            messages.success(request, "Tu mensaje ha sido enviado a los administradores.")
            return redirect('home_view')
    else:
        form = MensajePropietarioForm()
    context = {'form': form}
    return render(request, 'locales/enviar_mensaje.html', context)