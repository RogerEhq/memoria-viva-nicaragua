from django.db import models
from django.contrib.auth.models import User

# Modelo para Eventos Culturales
class EventoCultural(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion_texto = models.CharField(max_length=255)
    publicado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='eventos_creados')

    def __str__(self):
        return self.nombre
