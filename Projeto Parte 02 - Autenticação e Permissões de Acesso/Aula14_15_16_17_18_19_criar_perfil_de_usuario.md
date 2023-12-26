# **Criar Perfil de Usuário**

**Dev: Letícia Lima**

Já que estamos no embalo de contas e autenticação vamos aproveitar e criar um perfil para usuário. 

```python
python manage.py startapp perfil
```

Registrar seu app no settings do projeto e colocar na pasta apps.

```python
PROJECT_APPS = [
    'apps.base',
    'apps.perfil', # adicionar
]
```

apps/perfil/models.py

```python
from django.conf import settings
from django.db import models

class Perfil(models.Model):   
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='perfil') 
    foto = models.ImageField(upload_to='perfil/foto/', default='perfil/foto-padrao.png', blank=True)  
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
```

apps/perfil/admin.py

```python
from perfil.models import Perfil

# Register your models here.
admin.site.register(Perfil)
```

Agora vamos adicionar uma instancia para perfil toda vez que criarmos um usuário no sistema.

Documentação: https://docs.djangoproject.com/en/4.2/topics/signals/

https://docs.djangoproject.com/en/4.2/ref/signals/

Os Signals em Django são uma forma de permitir que determinadas ações (como criar, editar ou excluir um objeto) disparem uma função que pode executar ações adicionais no momento em que essas ações ocorrem.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver 

class Perfil(models.Model):   
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil') 
...
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_perfil(sender, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.create(usuario=kwargs['instance'])
```

### **Alternativa que gosto de usar.**

Podemos simplesmente colocar na views para criar essa instancia. 

```python
Perfil.objects.create(usuario=usuario) # Cria instancia perfil do usuário
```

Por exemplo a views de criar um novo usuário no sistema. Podemos colocar essa regra para criar uma instancia na tabela de perfil para o novo usuário.

apps/contas/views.py

```python
def register_view(request):
    ...
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()
            
            Perfil.objects.create(usuario=usuario) # Cria instancia perfil do usuário
            
           ...
```

---

## Vamos criar um template para exibir perfil.

documentação: https://docs.djangoproject.com/en/4.2/ref/models/querysets/

procure por select_related.

O método **`select_related`** é usado para pré-carregar os objetos relacionados em um modelo ForeignKey ou OneToOne de uma única consulta ao banco de dados, em vez de executar consultas adicionais para recuperar cada objeto relacionado.

Por exemplo, se um objeto de modelo A tem uma ForeignKey para um objeto de modelo B e você usa **`select_related`** em A, o Django carregará B junto com A em uma única consulta ao banco de dados. Isso é útil quando você precisa acessar as informações de B, mas não deseja executar consultas adicionais para recuperá-las.

Note que o **`select_related`** só funciona com chaves estrangeiras e não funciona com campos ManyToMany.

apps/perfil/views.py

```python
from django.shortcuts import get_object_or_404, render
from contas.models import MyUser

def perfil_view(request, id):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), id=id)
    context = {'obg': perfil}
    return render(request, 'perfil.html', context)
```

apps/perfil/urls.py

```python
from django.urls import path
from perfil.views import perfil_view

urlpatterns = [
    path('<int:id>/', perfil_view, name='perfil'),
]
```

Lembrando eu já to aplicando algumas class bootstrap que conheço. Pra deixar bonitinho.

apps/perfil/templates/perfil.html

```python
{% extends "base.html" %}
{% block content %} 
<div class="container mt-3">
    <div class="d-flex flex-wrap gap-5 justify-content-center align-items-center">
        <div class="d-flex flex-column">  
            <img src="{{obj.perfil.foto.url}}" class="img-thumbnail border rounded" width="280" alt="">  
            <button class="btn btn-warning" onclick="location.href='#'">
                <i class="fas fa-cog"></i> Editar Perfil
            </button>
        </div> 
        <div class="perfil-info mt-3"> 
            <h2>{{obj.first_name}} {{obj.last_name}}</h2>
            <p><strong>Data Criação:</strong> {{obj.date_joined|date:'d/m/Y'}}</p>
            <p><strong>Ocupação:</strong> {{obj.perfil.ocupacao}}</p>
            <p><strong>Descrição:</strong> {{obj.perfil.descricao}}</p>
            <p><strong>Genero:</strong> {{obj.perfil.genero}}</p>
            <div class="d-flex gap-3"> 
                <p><strong>Telefone:</strong> {{obj.perfil.telefone}}</p>
                <p><strong>Cidade:</strong> {{obj.perfil.cidade}}</p>
                <p><strong>País:</strong> {{obj.perfil.estado}}</p>   
            </div>
        </div>
    </div> 
    <hr>
</div>
{% endblock %}
```

---

## **Chamar o `username` na URL**

Nota que, estamos usando o id no parametro da url para acessar o perfil. 

**Como fazer para ser o username ?**

Primeiramente, é importante entender que no modelo de **`MyUser`** que estamos utilizando para criar usuários, não temos um campo **`username`** definido. Isso ocorre porque estamos utilizando o email como principal username e único.

Entretanto, para evitar a presença de um "@" no username que aparece na URL, vamos criar um campo personalizado para o **`username`**, somente para esse propósito. E para fazer a criação automática do **`username`**, vamos utilizar o email do usuário como base para gerar esse campo.

vamos lá, primeiro remos que criar um campo chamado username por que não temos.

apps/contas/models.py

```python
import re

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True,blank=True)
	...

	def save(self, *args, **kwargs):
        get_email = self.email.split("@")[0]
        email = re.sub(r"[^a-zA-Z0-9]","",get_email)
        self.username = email
        super(MyUser, self).save(*args, **kwargs)
```

 

lembrando que agora todos os usuarios precisam ter um nome de username para acessar o perfil. Os novos seram gerados automaticos mas os antigos temos que criar.

apps/perfil/views.py 

```python
from django.shortcuts import get_object_or_404, render
from contas.models import MyUser

def perfil_view(request, username):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), username=username)
    context = {'obg': perfil}
    return render(request, 'perfil.html', context)
```

apps/perfil/urls.py

```python
from django.urls import path
from perfil.views import perfil_view

urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
]
```

criei um usuario novo 

http://localhost:8000/perfil/joao/

Podemos aproveitar e mudar na rota de atualizar um usuario. Adicionamos o username.

```python
# views.py
def atualizar_usuario(request, username):
    user = get_object_or_404(MyUser, username=username)

#urls.py
path('atualizar-usuario/<slug:username>/',  views.atualizar_usuario, name='atualizar_usuario'),
```

---

### E os registros existentes ?

Para os registros existentes se voce pode apagar e adicionar novamente, ok. Mas vamos suporte que voce tenha uma base de dados grande e precisa fazer uma modificação em massa. Nesse caso vamos fazer um script.

Vamos utilizar o command do proprio django e criar um handler. 

https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/

Cria esse script para fazer essa modificação.

apps/contas/management/commands/criaUsername.py

```python
import re
from django.core.management.base import BaseCommand
from contas.models import MyUser

class Command(BaseCommand):
    help = "Atualizar o Cadastro de usuario adicionando username"
    
    def handle(self, *args, **options):
        myuser = MyUser.objects.all()
        for user in myuser:
             
            get_email = user.email.split("@")[0]
            email = re.sub(r"[^a-zA-Z0-9]","",get_email)
            user.username = email
            user.save()

            self.stdout.write(
                self.style.SUCCESS('username Atualizado com sucesso "%s"' % user.username)
            )
```

para rodar esse script 

```python
python manage.py criaUsername
```

Feito essa modificação, já podemos testar a rota do perfil.

http://localhost:8000/perfil/leticia/

apps/base/templates/components/navbar.html
```python
...
<span class="p-2">
    <a class="nav-link" href="{% url 'perfil' user.username %}">
        <i class="fas fa-user mx-2"></i>{{user.first_name}} {{user.last_name}}
    </a>
</span>
...
```