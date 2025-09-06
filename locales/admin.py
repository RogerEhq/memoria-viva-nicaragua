from django.contrib import admin
from .models import Local, Relato, Negocio, SugerenciaNegocio

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'propietario')
    search_fields = ('nombre', 'departamento')

@admin.register(Relato)
class RelatoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'content')
    actions = ['approve_relatos', 'reject_relatos']

    def approve_relatos(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Los relatos seleccionados han sido aprobados.")
    approve_relatos.short_description = "Aprobar relatos seleccionados"

    def reject_relatos(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Los relatos seleccionados han sido rechazados.")
    reject_relatos.short_description = "Rechazar relatos seleccionados"

@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(SugerenciaNegocio)
class SugerenciaNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre_negocio', 'sugerido_por', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre_negocio',)
    actions = ['aprobar_sugerencia_y_crear_negocio']

    def aprobar_sugerencia_y_crear_negocio(self, request, queryset):
        for sugerencia in queryset:
            if sugerencia.estado == 'pending':
                Negocio.objects.create(
                    name=sugerencia.nombre_negocio,
                    description=sugerencia.comentarios,
                    address_text=sugerencia.ubicacion_texto,
                    created_by=sugerencia.sugerido_por,
                    category='restaurante'
                )
                sugerencia.estado = 'approved'
                sugerencia.save()
        self.message_user(request, "Sugerencias seleccionadas aprobadas y negocios creados.")
    aprobar_sugerencia_y_crear_negocio.short_description = "Aprobar y crear negocio"
