from django.contrib import admin
from .models import EventoCultural

@admin.register(EventoCultural)
class EventoCulturalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion_texto', 'publicado_por')
    list_filter = ('fecha_inicio',)
    search_fields = ('nombre', 'descripcion', 'ubicacion_texto')
