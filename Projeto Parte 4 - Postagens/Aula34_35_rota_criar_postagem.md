# **Rota Criar Postagem**

**Dev: Letícia Lima**

Eu geralmente tenho o costume de tratar qualquer tipo de formulário com django usando o forms. 

Crio uma classe no forms e trato as diferenças de campo. Assim não polui muito o template no html e centraliza os problemas de formulário no ali na classe. 

Então cria uma class com os campos, como voces podem ver **data_publicacao** está recebendo um tratamento diferente. E temos um iniciador que adiciona a class bootstrap em todos os campos.

apps/forum/forms.py

```python
from django import forms
from django.conf import settings
from .models import PostagemForum

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'})) 
    class Meta:
        model = PostagemForum
        fields = ['usuario', 'titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForumForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
```

Na views vamos adicionar uma função para criar essas postagens. Nessa view se metodo é post ele pega o nosso `**PostagemForumForm**` que criamos no forms.py e verifica todas as validações que fizemos. Se tudo ok, salva e redireciona para lista de postagens no homepage *(Por enquanto, depois vamos adicionar essa lista no dashboard)*
apps/forum/views.py

```python
from django.shortcuts import render, redirect
from forum.forms import PostagemForumForm
from django.contrib import messages  

def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
            messages.success(request, 'Seu Post foi cadastrado com sucesso!')
            return redirect('lista-postagem-forum')
    return render(request, 'form-postagem-forum.html', {'form': form})
```

apps/forum/urls.py

```python
from django.urls import path 
from forum import views

urlpatterns = [
    ...
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),
]
```

Nosso template fica assim. Esse `**{{form}}**` contem todos os campos do nosso formulário que tratamos em forms. O **`as_p adiciona o <p>`**. Como podem percebe estamos herdando de **`base_dashboard.html`**

apps/forum/templates/form-postagem-forum.html

```html
{% extends "base_dashboard.html" %}
{% block title %}Criar uma Postagem{% endblock %}
{% block content_dash %}
<div class="row"> 
    <div class="col-md-8">
        <form class="p-3 rounded-3 shadow-sm" method="post" 
							enctype="multipart/form-data">
            {% csrf_token %}
            <h4>Criar Postagem</h4>
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary mx-2">Criar</button>
        </form>
    </div> 
</div> 
{% endblock %}
```

Na navbar adicionamos um botão para redirecionar o usuario para criar uma postagem.

apps/base/templates/components/navbar.html

```html
{% if user.is_authenticated %}
<button class="btn btn-success mx-2" 
			onclick="location.href='{% url 'criar-postagem-forum' %}'">
    <i class="fas fa-plus"></i> Criar Postagem</button>
...
```

### Remover o campo usuario do forms

```python
class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'},)
        )  
    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']
```

Na **views.py** adicionamos o campo usuario para pegar o **request.user** automatico.
```
def cadastrar_postagem(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user
            forum.save()
...
```