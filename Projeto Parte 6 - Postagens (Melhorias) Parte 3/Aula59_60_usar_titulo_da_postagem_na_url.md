# **Usar titulo da postagem na URL**

**Dev: Letícia Lima**

Como vocês perceberam estamos passando o **ID na URL** para fazer os eventos que precisamos. Seria interessante passar uma string como titulo por exemplo.

Para fazer isso no modelo precisamos fazer algumas modificações. Vamos adicionar um slug unique. Para não existir titulo igual, assim não ocorre conflitos. E no **save()** podemos tratar assim.

https://docs.djangoproject.com/en/4.2/ref/models/fields/

apps/forum/models.py

```python
from django.utils.text import slugify

class PostagemForum(models.Model):
    titulo = models.CharField(max_length=100)
    # Outros campos do modelo...

    slug = models.SlugField(unique=True, null=True)  # Campo de slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)  # Gera o slug com base no título
        super().save(*args, **kwargs)
```

Pode acontecer de aparecer titulo igual do jeito que está ai ele avisa por que o campo slug está com unique. Mas podemos fazer um tratamento diferente, como esse slug é gerado automatico podemos colocar uma regra. 

Esse string é incrivel, vocês podem ver a documentação. Basicamente nessa variavel “random_string” estamos gerando automaticamente uma string de 5 caracter e adicionando com titulo.

```python
import random
import string

def save(self, *args, **kwargs):
	if not self.slug:  # Executa apenas se o campo 'slug' estiver vazio
	    slug_base = slugify(self.titulo)  # Gera o slug com base no título
	    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Gera uma string aleatória de 5 caracteres
	    self.slug = f"{slug_base}-{random_string}"  # Adiciona a string aleatória ao slug base
	super().save(*args, **kwargs)
```

Depois de rodar o makemigrations e migrate. Vamos precisar mudar nossas views relacionadas com postagens. Então fiquem atentos aos apps forum e perfil. **E vamos atualizar o template onde passamos o parametro ID que agora será slug e views que recebe ID da postagem agora será slug.**

apps/forum/views.py

```python
# Detalhes postagem
def detalhe_postagem_forum(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
		...

# Editar Postagem
@login_required 
def editar_postagem_forum(request,slug):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
		...

# Deletar Postagem
@login_required 
def deletar_postagem_forum(request, slug): 
    redirect_route = request.POST.get('redirect_route', '')
    print(redirect_route)
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
		...

```

apps/forum/url.py

```python
path('detalhe-postagem-forum/<str:slug>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
path('editar-postagem-forum/<str:slug>/', views.editar_postagem_forum, name='editar-postagem-forum'),
path('deletar-postagem-forum/<str:slug>/', views.deletar_postagem_forum, name='deletar-postagem-forum'),
```

apps/forum/templates/* **forum e perfil que usa rota para app forum.**

```python
{% url 'detalhe-postagem-forum' postagem.slug %}
{% url 'deletar-postagem-forum' postagem.slug %}
{% url 'editar-postagem-forum' postagem.slug %}
```

<aside>
⚠️ **Outro ponto são as postagens que já existem certo ?** Elas vão estar sem slug e isso pode ocorrer erros. Para tratar isso podemos fazer um script para atualizar todas as postagens existente. É muito simples basicamente precisamos salvar o objeto novamente para clicar o slug. Voce pode fazer isso manualmente abrindo e salvando uma a uma. Ou pode user esse script que vou deixar pra voces.

</aside>

uma opção é simplesmente salvar cada postagem individualmente. Ao chamar o método **`save()`** em uma instância de **`PostagemForum`**, o slug será gerado automaticamente com base no título atualizado.

apps/forum/management/commands/criaSlugPostagens.py

```python
from django.core.management.base import BaseCommand
from forum.models import PostagemForum

class Command(BaseCommand):
    help = "Atualizar os slugs das postagens que não possuem slug"

    def handle(self, *args, **options):
        postagens = PostagemForum.objects.all()

        for postagem in postagens:
            postagem.save()

        self.stdout.write(self.style.SUCCESS('Os slugs foram atualizados com sucesso!'))
```

Para rodar o script 

```python
python manage.py criaSlugPostagens
```

**Outro detalhe eu não gosto de deixar o campo slug editavel no Admin Django.** 

Faço isso. Adiciona **`readonly_filed`** e coloca slug.

```python
class PostagemForumAdmin(admin.ModelAdmin):
    inlines = [
        PostagemForumImageInline,
    ]
    readonly_fields = ('slug',)
```

**Bem legal pessoal, fica muito profissional.**