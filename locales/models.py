from django.db import models
from django.contrib.auth.models import User


class Local(models.Model):
    nombre = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Relato(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField(default= '')
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
