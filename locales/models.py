from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.html import format_html
from django.db.models import Avg
from django.utils import timezone


# Nuevo modelo para las categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


# Rango de usuario, se usará en PerfilUsuario
class Rango(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Rangos"


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfilusuario')
    avatar = models.ImageField(upload_to='avatares/', default='avatares/default_avatar.png')
    rango = models.ForeignKey(Rango, on_delete=models.SET_NULL, null=True, blank=True)
    biografia = models.TextField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Asegura que siempre se asigne un rango por defecto al crear un nuevo usuario
        rango_defecto, _ = Rango.objects.get_or_create(nombre='Visitante')
        PerfilUsuario.objects.get_or_create(usuario=instance, rango=rango_defecto)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfilusuario.save()


# Modelo para Relatos
class Relato(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatos')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='relatos_images/', blank=True, null=True)

    # ¡NUEVOS CAMPOS AGREGADOS!
    ubicacion_texto = models.CharField(max_length=255, verbose_name="Ubicación en el mapa", blank=True, null=True)
    latitud = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitud = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)

    def __str__(self):
        return self.title


# Modelo para Negocios (Locales)
class Negocio(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Negocio")
    description = models.TextField(verbose_name="Descripción")
    address_text = models.CharField(max_length=255, verbose_name="Dirección")
    hours = models.CharField(max_length=100, blank=True, null=True, verbose_name="Horario")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='negocios_creados')
    propietario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='negocios_propios')
    foto_principal = models.ImageField(upload_to='negocios_fotos/', blank=True, null=True,
                                       verbose_name="Foto Principal")
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    categoria_relacionada = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name="Categoría")
    paquetes_turismo = models.TextField(blank=True, null=True, verbose_name="Paquetes de Turismo")
    video_url = models.URLField(max_length=200, blank=True, null=True,
                                verbose_name="Enlace de video (YouTube, Vimeo, etc.)")

    # ¡NUEVOS CAMPOS AÑADIDOS!
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Correo Electrónico")
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name="Página Web")
    is_turismo = models.BooleanField(default=False, verbose_name="Es un negocio de turismo")

    propietario_contacto = models.CharField(max_length=100, blank=True, null=True,
                                            verbose_name="Información de Contacto del Propietario")

    def __str__(self):
        return self.name

    def update_calificacion_promedio(self):
        avg_rating = self.calificacion_set.aggregate(Avg('puntuacion'))['puntuacion__avg']
        self.calificacion_promedio = round(avg_rating, 2) if avg_rating else 0.0
        self.save()


# Modelo para Sugerencia de Negocio
class SugerenciaNegocio(models.Model):
    ESTADO_OPCIONES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ]
    nombre_negocio = models.CharField(max_length=100)
    ubicacion_texto = models.CharField(max_length=255, verbose_name="Ubicación")
    latitud = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitud = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    sugerido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sugerencias')
    fecha_sugerencia = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='pending')
    foto_referencia = models.ImageField(upload_to='sugerencias_fotos/', blank=True, null=True)
    foto_aprobada = models.BooleanField(default=False)
    categoria_relacionada = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name="Categoría sugerida")

    def __str__(self):
        return f"Sugerencia: {self.nombre_negocio}"

    class Meta:
        verbose_name_plural = "Sugerencias de Negocio"
        ordering = ['-fecha_sugerencia']


# Modelo para Recetas
class Receta(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    ingredientes = models.TextField(help_text="Lista de ingredientes, separados por comas o saltos de línea.")
    pasos = models.TextField(help_text="Instrucciones paso a paso.")
    imagen = models.ImageField(upload_to='recetas_imagenes/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recetas')
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Recetas"


# Modelo para Saber Popular
class SaberPopular(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='saberes_imagenes/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Saberes Populares"


# Modelo para Comentarios
class Comentario(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.negocio.name}"

    class Meta:
        verbose_name_plural = "Comentarios"


# Modelo para Calificaciones
class Calificacion(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    fecha = models.DateTimeField(default=timezone.now)
    comentario = models.OneToOneField(Comentario, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='calificacion')

    def __str__(self):
        return f"Calificación de {self.puntuacion} de {self.usuario.username} para {self.negocio.name}"

    class Meta:
        verbose_name_plural = "Calificaciones"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.negocio.update_calificacion_promedio()


# Modelo para Reclamo de Negocio
class ReclamoNegocio(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, verbose_name="Negocio a reclamar")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuario que reclama")
    contrato_pdf = models.FileField(upload_to='reclamos/', blank=True, null=True, verbose_name="Documento de propiedad")
    mensaje = models.TextField(verbose_name="Mensaje para el administrador")
    aprobado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reclamo de {self.usuario.username} para {self.negocio.name}"

    class Meta:
        verbose_name_plural = "Reclamos de Negocio"


# Modelo para Reporte de Comentario
class ReporteComentario(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    motivo = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reporte de {self.usuario.username} en {self.comentario.id}"

    class Meta:
        verbose_name_plural = "Reportes de Comentario"


# NUEVO: Modelo para mensajes de propietarios a administradores
class MensajePropietario(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    asunto = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.propietario.username}: {self.asunto}"

    class Meta:
        verbose_name_plural = "Mensajes de Propietarios"
        ordering = ['-fecha_envio']