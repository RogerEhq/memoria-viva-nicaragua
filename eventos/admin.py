from django.contrib import admin
from .models import EventoCultural

@admin.register(EventoCultural)
class EventoCulturalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion_texto', 'publicado', 'publicado_por')
    list_filter = ('publicado', 'fecha_inicio')
    search_fields = ('nombre', 'descripcion', 'ubicacion_texto')
    actions = ['aprobar_eventos', 'ocultar_eventos']

    def aprobar_eventos(self, request, queryset):
        queryset.update(publicado=True)
        self.message_user(request, "Eventos seleccionados publicados.")
    aprobar_eventos.short_description = "✅ Publicar eventos seleccionados"

    def ocultar_eventos(self, request, queryset):
        queryset.update(publicado=False)
        self.message_user(request, "Eventos seleccionados ocultados.")
    ocultar_eventos.short_description = "🚫 Ocultar eventos seleccionados"

