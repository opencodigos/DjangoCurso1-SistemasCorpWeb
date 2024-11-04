import random
import string
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model 

user = get_user_model()

# Create your models here.
class PostagemForum(models.Model):
    usuario = models.ForeignKey(user, related_name="user_postagem_forum", on_delete=models.CASCADE)  
    titulo = models.CharField('Titulo',max_length=100)
    descricao = models.TextField('Descrição',max_length=350) 
    data_publicacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField('Publicar Postagem?', default=False)
    anexar_imagem = models.ImageField('Imagem Anexo', upload_to='postagem-forum/', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)  # Campo de slug
     
    def __str__(self):
        return "{} ({})".format(self.titulo, self.data_publicacao)

    class Meta:
        verbose_name = 'Postagem Forum'
        verbose_name_plural = 'Postagem Forum'
        ordering = ['-data_criacao']
        
    def save(self, *args, **kwargs):
        if not self.slug:  # Executa apenas se o campo 'slug' estiver vazio
            slug_base = slugify(self.titulo)  # Gera o slug com base no título
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Gera uma string aleatória de 5 caracteres
            self.slug = f"{slug_base}-{random_string}"  # Adiciona a string aleatória ao slug base
        super().save(*args, **kwargs)  
        
         
class PostagemForumImagem(models.Model):
    imagem = models.FileField('Imagem Anexo', upload_to='postagem-forum/')
    postagem = models.ForeignKey(PostagemForum, related_name='postagem_imagens', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.postagem.titulo
    
    def clean(self):
        super().clean()
        if self.postagem.postagem_imagens.count() >= 5: # Limitar somente 5 anexos
            raise ValidationError('Você só pode adicionar no máximo 5 anexos.')