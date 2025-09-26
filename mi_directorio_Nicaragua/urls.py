from django.contrib import admin
from django.urls import path, include
from locales.views import home_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),  # Vista principal
    path('eventos/', include('eventos.urls')),
    path('locales/', include('locales.urls')),  # Rutas de la app locales
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
