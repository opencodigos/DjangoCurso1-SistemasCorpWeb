from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.db import models

class Perfil(models.Model):   
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, related_name='perfil') 
    foto = models.ImageField(upload_to='perfil/foto/', blank=True)  
    ocupacao = models.CharField(max_length=120, blank=True)
    descricao = models.TextField(blank=True)  
    genero = models.CharField(max_length=20, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, blank=True) 

    def __str__(self):
        return f' Perfil: {self.usuario.email}'

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"
        
        
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_perfil(sender, **kwargs): 
#     if kwargs.get('created', False):
#         Perfil.objects.create(usuario=kwargs['instance'])