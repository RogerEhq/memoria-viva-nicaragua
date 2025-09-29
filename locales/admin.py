from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Relato, Negocio, SugerenciaNegocio, Receta,
    PerfilUsuario, Comentario, Calificacion,
    ReclamoNegocio, ReporteComentario, Categoria, MensajePropietario
)


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
    list_display = (
        'name',
        'categoria_relacionada',
        'is_turismo',  # <--- NUEVO: Muestra si es de turismo
        'created_by',
        'vista_foto'
    )
    list_filter = ('categoria_relacionada',)
    search_fields = ('name',)
    readonly_fields = ('vista_foto_detalle',)
    fields = (
        'name',
        'description',
        'categoria_relacionada',
        'address_text',
        'hours',
        'created_by',
        'propietario',
        'foto_principal',
        'vista_foto_detalle',
        'calificacion_promedio',
        'paquetes_turismo'  # <--- NUEVO: Campo para editar
    )

    def vista_foto(self, obj):
        if obj.foto_principal:
            return format_html('<img src="{}" width="100" style="border-radius:6px;" />', obj.foto_principal.url)
        return "Sin imagen"

    vista_foto.short_description = "Foto principal"

    def vista_foto_detalle(self, obj):
        if obj.foto_principal:
            return format_html('<img src="{}" width="300" style="border-radius:10px;" />', obj.foto_principal.url)
        return "Sin imagen"

    vista_foto_detalle.short_description = "Vista ampliada"


@admin.register(SugerenciaNegocio)
class SugerenciaNegocioAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_negocio', 'sugerido_por', 'estado',
        'categoria_relacionada', 'foto_aprobada', 'vista_previa'
    )
    list_filter = ('estado', 'categoria_relacionada', 'foto_aprobada')
    search_fields = ('nombre_negocio', 'sugerido_por__username')
    readonly_fields = ('mostrar_foto', 'fecha_sugerencia')
    fields = (
        'nombre_negocio', 'ubicacion_texto', 'comentarios', 'sugerido_por',
        'estado', 'categoria_relacionada',
        'foto_referencia', 'mostrar_foto', 'foto_aprobada'
    )
    actions = ['aprobar_sugerencia_y_crear_negocio', 'aprobar_foto_referencia']

    def mostrar_foto(self, obj):
        if obj.foto_referencia:
            return format_html('<img src="{}" width="300" style="border-radius:10px;" />', obj.foto_referencia.url)
        return "Sin imagen"

    mostrar_foto.short_description = "Vista previa"

    def vista_previa(self, obj):
        if obj.foto_referencia:
            return format_html('<img src="{}" width="100" style="border-radius:6px;" />', obj.foto_referencia.url)
        return "Sin imagen"

    vista_previa.short_description = "Miniatura"

    def aprobar_sugerencia_y_crear_negocio(self, request, queryset):
        creados = 0
        actualizados = 0
        for sugerencia in queryset:
            try:
                negocio_existente = Negocio.objects.filter(name=sugerencia.nombre_negocio).first()
                if negocio_existente:
                    negocio_existente.description = sugerencia.comentarios
                    negocio_existente.address_text = sugerencia.ubicacion_texto
                    # Asegurarse de que el campo de categoría se actualiza correctamente
                    if sugerencia.categoria_relacionada:
                        negocio_existente.categoria_relacionada = sugerencia.categoria_relacionada
                    if sugerencia.foto_aprobada:
                        negocio_existente.foto_principal = sugerencia.foto_referencia
                    negocio_existente.save()
                    actualizados += 1
                else:
                    Negocio.objects.create(
                        name=sugerencia.nombre_negocio,
                        description=sugerencia.comentarios,
                        address_text=sugerencia.ubicacion_texto,
                        created_by=sugerencia.sugerido_por,
                        categoria_relacionada=sugerencia.categoria_relacionada,
                        foto_principal=sugerencia.foto_referencia if sugerencia.foto_aprobada else None
                    )
                    creados += 1
                sugerencia.estado = 'approved'
                sugerencia.save()
            except Exception as e:
                self.message_user(request, f"Error al procesar sugerencia: {e}", level='error')
        self.message_user(request, f"{creados} negocio(s) creados, {actualizados} actualizado(s).")

    def aprobar_foto_referencia(self, request, queryset):
        actualizadas = 0
        for sugerencia in queryset:
            if sugerencia.foto_referencia and not sugerencia.foto_aprobada:
                sugerencia.foto_aprobada = True
                sugerencia.save()
                actualizadas += 1
                negocio_existente = Negocio.objects.filter(name=sugerencia.nombre_negocio).first()
                if negocio_existente:
                    negocio_existente.foto_principal = sugerencia.foto_referencia
                    negocio_existente.save()
        self.message_user(request, f"{actualizadas} foto(s) aprobadas y vinculadas a negocios existentes.")

    aprobar_foto_referencia.short_description = "Aprobar foto(s) de referencia"


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'ingredientes', 'autor__username')
    actions = ['aprobar_recetas', 'rechazar_recetas']

    def aprobar_recetas(self, request, queryset):
        queryset.update(estado='approved')
        self.message_user(request, "Las recetas seleccionadas han sido aprobadas.")

    aprobar_recetas.short_description = "Aprobar recetas seleccionadas"

    def rechazar_recetas(self, request, queryset):
        queryset.update(estado='rejected')
        self.message_user(request, "Las recetas seleccionadas han sido rechazadas.")

    rechazar_recetas.short_description = "Rechazar recetas seleccionadas"


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rango', 'ubicacion', 'telefono')
    list_filter = ('rango',)
    search_fields = ('usuario__username', 'ubicacion', 'telefono')
    readonly_fields = ('usuario',)
    fields = ('usuario', 'rango', 'avatar', 'biografia', 'telefono', 'ubicacion')


@admin.register(ReclamoNegocio)
class ReclamoAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'usuario', 'aprobado', 'fecha_envio')
    list_filter = ('aprobado',)
    actions = ['aprobar_reclamos']

    def aprobar_reclamos(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, "Los reclamos seleccionados han sido aprobados.")

    aprobar_reclamos.short_description = "Aprobar reclamos seleccionados"


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'usuario', 'texto', 'fecha')
    readonly_fields = ('negocio', 'usuario', 'texto', 'fecha')

    def has_add_permission(self, request):
        return False


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'usuario', 'puntuacion')
    readonly_fields = ('negocio', 'usuario', 'puntuacion')

    def has_add_permission(self, request):
        return False


@admin.register(ReporteComentario)
class ReporteComentarioAdmin(admin.ModelAdmin):
    list_display = ('comentario', 'usuario', 'motivo', 'fecha')
    search_fields = ('comentario__texto', 'usuario__username', 'motivo')
    list_filter = ('fecha',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'slug')


# Registramos el modelo MensajePropietario para que aparezca en el panel de administración
admin.site.register(MensajePropietario)