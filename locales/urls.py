from django.contrib import admin
from django.urls import path, include
from locales import views as locales_views
from .views import create_receta_view

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', locales_views.home_view, name='home_view'),
    path('register/', locales_views.register_view, name='register_view'),
    path('login/', locales_views.login_view, name='login_view'),
    path('logout/', locales_views.logout_view, name='logout_view'),
    path('relatos/crear/', locales_views.create_relato_view, name='create_relato_view'),
    path('directorio/sugerir/', locales_views.sugerir_negocio_view, name='sugerir_negocio_view'),
    path('mostrar_mapa/', locales_views.mostrar_mapa, name='mostrar_mapa'),
    path('create_receta/', create_receta_view, name='create_receta_view'),

    path('perfil/', locales_views.editar_perfil, name='perfil_view'),
    path('perfil/eliminar-avatar/', locales_views.eliminar_avatar, name='eliminar_avatar'),

    # 📚 Nuevas rutas para la Biblioteca
    path('biblioteca/', locales_views.biblioteca_view, name='biblioteca_view'),

    # 🗓️ Nuevas rutas para el Calendario Cultural
    path('eventos/', include('eventos.urls')),

    path('usuarios/', locales_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<str:username>/', locales_views.perfil_publico, name='perfil_publico'),
    path('juego/', views.juego_view, name='juego_view'),

    path('local/<int:negocio_id>/', locales_views.detalle_negocio, name='detalle_negocio'),

    path('reclamar-negocio/', locales_views.reclamar_negocio, name='reclamar_negocio'),

    path('negocios/', locales_views.lista_negocios, name='lista_negocios'),


    path('local/<int:negocio_id>/comentario/', locales_views.detalle_negocio, name='agregar_comentario'),
    path('local/<int:negocio_id>/calificacion/', locales_views.detalle_negocio, name='agregar_calificacion'),

    path('comentario/<int:comentario_id>/reportar/', locales_views.reportar_comentario, name='reportar_comentario'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)