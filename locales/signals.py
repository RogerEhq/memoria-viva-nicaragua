from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario, Rango

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        rango_defecto, _ = Rango.objects.get_or_create(nombre='Visitante')
        PerfilUsuario.objects.get_or_create(usuario=instance, rango=rango_defecto)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfilusuario.save()