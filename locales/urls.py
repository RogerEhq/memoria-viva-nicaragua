from django.contrib import admin
from django.urls import path, include
from locales import views as locales_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', locales_views.home_view, name='home_view'),
    path('register/', locales_views.register_view, name='register_view'),
    path('login/', locales_views.login_view, name='login_view'),
    path('logout/', locales_views.logout_view, name='logout_view'),
    path('relatos/crear/', locales_views.create_relato_view, name='create_relato_view'),
    path('directorio/sugerir/', locales_views.sugerir_negocio_view, name='sugerir_negocio_view'),
    path('mostrar_mapa/', locales_views.mostrar_mapa, name='mostrar_mapa'),
    path('create_receta/', locales_views.create_receta_view, name='create_receta_view'),
    path('perfil/', locales_views.editar_perfil, name='perfil_view'),
    path('perfil/eliminar-avatar/', locales_views.eliminar_avatar, name='eliminar_avatar'),
    path('biblioteca/', locales_views.biblioteca_view, name='biblioteca_view'),
    path('eventos/', include('eventos.urls')),
    path('usuarios/', locales_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<str:username>/', locales_views.perfil_publico, name='perfil_publico'),
    path('juego/', locales_views.juego_view, name='juego_view'),
    path('negocios/', locales_views.lista_negocios, name='lista_negocios'),
    path('negocios/<slug:categoria_slug>/', locales_views.lista_negocios, name='lista_negocios_por_categoria'),
    path('local/<int:negocio_id>/', locales_views.detalle_negocio, name='detalle_negocio'),
    path('reclamar-negocio/', locales_views.reclamar_negocio, name='reclamar_negocio'),
    path('plan-turismo/', locales_views.plan_turismo, name='plan_turismo'),
    path('negocios/<int:negocio_id>/paquetes/', locales_views.detalle_paquetes_turismo,
         name='detalle_paquetes_turismo'),
    path('negocios/<int:negocio_id>/editar-paquetes/', locales_views.editar_paquetes_turismo,
         name='editar_paquetes_turismo'),
    path('comentario/<int:comentario_id>/reportar/', locales_views.reportar_comentario, name='reportar_comentario'),
    path('local/<int:negocio_id>/comentar-y-calificar/', locales_views.comentar_y_calificar,
         name='comentar_y_calificar'),
    path('negocio/editar/<int:pk>/', locales_views.editar_negocio, name='editar_negocio'),
    path('mensajes/enviar/', locales_views.enviar_mensaje_admin, name='enviar_mensaje_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)