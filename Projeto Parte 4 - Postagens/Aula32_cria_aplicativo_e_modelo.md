# **Criando Aplicativo e Modelo**

**Dev: Letícia Lima**

Vamos criar nosso App para gerenciar nossas postagens. Vou chamar de **`forum`**. Lá no inicio definimos que seria um site completo de uma organização e teremos um **forum fechado somente para clientes** onde teriam perguntas e resposta (resolver as duvidas em gerais).

```python
python manage.py startapp forum
```

Não podemos esquecer de register o site no core/settings.py

```python
THIRD_APPS = [
	  ...
    'apps.forum', # Adiciona
]
```

Criando o modelo. Utilizando como referencia o **StackOverflow** pretendo adicionar esses campos iniciais.
apps/forum/models.py
```python
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

user = get_user_model()

# Create your models here.
class PostagemForum(models.Model):
    usuario = models.ForeignKey(user, 
								related_name="user_postagem_forum", on_delete=models.CASCADE)  
    titulo = models.CharField('Titulo',max_length=100)
    descricao = models.TextField('Descrição',max_length=350) 
    data_publicacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField('Publicar Postagem?', default=False)
    anexar_imagem = models.ImageField('Imagem Anexo', 
							upload_to='postagem-forum/', blank=True, null=True)
    
    def __str__(self):
        return "{} ({})".format(self.titulo, self.data_publicacao)

		class Meta:
        verbose_name = 'Postagem Forum'
        verbose_name_plural = 'Postagem Forum'
        ordering = ['-data_criacao']
```