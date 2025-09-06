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
    # Nuevas URL para el contenido y el directorio
    path('relatos/crear/', locales_views.create_relato_view, name='create_relato_view'),
    path('directorio/sugerir/', locales_views.sugerir_negocio_view, name='sugerir_negocio_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)