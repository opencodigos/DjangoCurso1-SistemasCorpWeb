# **Rota Lista de Postagens**

**Dev: Letícia Lima**

Vamos criar uma função para listar todas as postagens inicialmente na homepage. Teremos um botão no menu da navbar “forum”.

apps/forum/views.py

```python
from django.shortcuts import render
from forum import models

# Create your views here.
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True)
    context = {'postagens': postagens}
    return render(request, 'lista-postagem-forum.html', context)
```

Registra na urls para conseguirmos acessar a rota.
apps/forum/urls.py

```
from django.urls import path 
from forum import views

urlpatterns = [
    path('', views.lista_postagem_forum, name='lista-postagem-forum'),
]
```

Na urls do projeto precisamos registrar para conseguir acessar essa função na view.

core/urls.py

```python
path('forum/', include('forum.urls')),
```

No template eu tenho mais ou menos pronto. Estou herdando o template base e criei uma lista simples com bootstrap. Segue modelo abaixo.
https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
apps/forum/templates/lista-postagem-forum.html

```html
{% extends "base.html" %}
{% block title %}Todos as Postagens do Forum{% endblock %}
{% block content %}
<div class="container mt-3">
	<div class="row">
	    <div class="col-md-8">
	        {% include 'components/messages.html' %}
	        {% for postagem in postagens %}
	        <div class="p-3 mb-3 rounded-3 shadow-sm">
	            <div class="align-items-center">
	                <div class="d-flex justify-content-between">
	                    <h5><a href="#">{{postagem.titulo}}</a></h5>
	                    <small>{{postagem.usuario.first_name}} {{postagem.usuario.last_name}}</small> 
	                </div>  
	                <div class="text-truncate-box"> 
	                    <p class="text-truncate">{{postagem.descricao|safe|truncatechars:230}}</p> 
	                </div>
	            </div>
	            <div class="d-flex justify-content-between align-items-center">
	                <div class="align-items-center">
	                    <small class="text-muted">{{postagem.data_publicacao}}</small>
	                </div>
	            </div>
	        </div> 
	        {% endfor %}
	    </div> 
	</div>
</div>
{% endblock %}
```

No componente da Navbar vamos adicionar o link para acessar essa lista de postagens.
apps/base/templates/components/navbar.html
```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'lista-postagem-forum' %}">Forum (QA)</a>
</li>
```