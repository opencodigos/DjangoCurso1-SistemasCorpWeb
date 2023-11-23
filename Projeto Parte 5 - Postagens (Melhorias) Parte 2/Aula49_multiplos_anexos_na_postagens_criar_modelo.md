# **Multiplos Anexos na Postagem (Bonus)** (Criar Modelo)

Dev: Letícia Lima

### Criar Modelo

**Ótimas novidades!** Para tornar as coisas mais interessantes, vamos criar uma nova funcionalidade que permitirá aos usuários fazer o upload de vários arquivos de uma vez. Vamos estabelecer algumas regras para isso. **Por exemplo, cada usuário poderá anexar no máximo 5 arquivos. Se já houver algum anexo, o usuário precisará identificar quantos arquivos já foram anexados e verificar se ainda faltam 5 arquivos para atingir o limite.**

Nessa implementação, utilizaremos a **AJAX apenas para a deletar as imagens**. Seria relativamente fácil criar uma postagem para salvar várias imagens. **No entanto, o desafio interessante consiste em mostrar visualmente como editar essas imagens.** Além disso, ofereceremos aos usuários a opção de remover completamente o anexo tanto do sistema quanto do banco de dados.

<aside>
💡 O que é AJAX?

AJAX, que significa "Asynchronous 't and XML"
(JavaScript e XML Assíncronos), é uma abordagem de
desenvolvimento web que permite que páginas web interajam
com o servidor em segundo plano, sem a necessidade de
recarregar a página inteira. Isso resulta em uma experiência
mais fluida e responsiva para os usuários.

</aside>

Vamos começar, primeiro precisamos criar um modelo de relacionamento **1 - N** com a tabela de postagem. Isso significa que uma postagem pode ter varios anexos.

apps/forum/models.py

```python
class PostagemForum(models.Model):
    usuario = models.ForeignKey(user, 
						related_name="user_postagem_forum", on_delete=models.CASCADE)  
   ...
    # anexar_imagem = models.ImageField('Imagem Anexo', upload_to='postagem-forum/', blank=True, null=True)

class PostagemForumImagem(models.Model):
    imagem = models.FileField('Imagem Anexo', upload_to='postagem-forum/')
    postagem = models.ForeignKey(PostagemForum, 
					related_name='postagem_imagens', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.postagem.titulo
    
    def clean(self):
        super().clean()
        if self.postagem.postagem_imagens.count() >= 5: # Limitar somente 5 anexos
            raise ValidationError('Você só pode adicionar no máximo 5 anexos.')
```

apps/forum/admin.py

**Para desmonstração no Django Admin:** 
https://docs.djangoproject.com/pt-br/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline

```python
from django.contrib import admin
from forum import models

class PostagemForumImagemInline(admin.TabularInline):
    model = models.PostagemForumImagem
    extra = 0

class PostagemForumAdmin(admin.ModelAdmin):
    inlines = [
        PostagemForumImagemInline,
    ]
    
# Register your models here.
admin.site.register(models.PostagemForum, PostagemForumAdmin)
# admin.site.register(models.PostagemForumImagem)
```

Inicialmente já conseguimos testar e ver como funciona. **Maximo 5 anexos.**
