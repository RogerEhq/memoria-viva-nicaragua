from django.db import models
from django.contrib.auth.models import User

class Relato(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    image = models.ImageField(upload_to='relatos/images/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Negocio(models.Model):
    CATEGORIES = (
        ('restaurante', 'Restaurante'),
        ('hotel', 'Hotel'),
        ('artesania', 'Artesanía'),
        ('museo', 'Museo'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    address_text = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='negocios_creados')
    propietario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='negocios_propios')
    foto_principal = models.ImageField(upload_to='negocios/', blank=True, null=True)
    calificacion_promedio = models.FloatField(default=0)

    def __str__(self):
        return self.name

class SugerenciaNegocio(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    )
    nombre_negocio = models.CharField(max_length=200)
    ubicacion_texto = models.TextField()
    comentarios = models.TextField()
    sugerido_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    fecha_sugerencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_negocio

class Receta(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ingredientes = models.TextField()
    pasos = models.TextField()
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class SaberPopular(models.Model):
    CATEGORIES = (
        ('dicho', 'Dicho'),
        ('leyenda', 'Leyenda'),
        ('mito', 'Mito'),
        ('costumbre', 'Costumbre'),
    )
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIES)
    contenido = models.TextField()
    estado = models.CharField(max_length=10, choices=SugerenciaNegocio.STATUS_CHOICES, default='pending')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saberes_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)

    RANGOS = [
        ('visitante', 'Visitante'),
        ('colaborador', 'Colaborador'),
        ('propietario', 'Propietario'),
        ('admin', 'Administrador'),
    ]
    rango = models.CharField(max_length=20, choices=RANGOS, default='visitante')

    def __str__(self):
        return f"{self.usuario.username} ({self.rango})"

class Comentario(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Calificacion(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.OneToOneField(Comentario, on_delete=models.CASCADE, null=True, blank=True)
    puntuacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

class ReclamoNegocio(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contrato_pdf = models.FileField(upload_to='contratos/')
    mensaje = models.TextField()
    aprobado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

class ReporteComentario(models.Model):
    comentario = models.ForeignKey('Comentario', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.comentario} por {self.usuario.username}"
