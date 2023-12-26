# Editar Perfil

Dev: Letícia Lima

### **Editar Perfil**

apps/perfil/forms.py

```python
from django import forms
from perfil.models import Perfil
    
class PerfilForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=200
    )
    class Meta:
        model = Perfil
        fields = ['foto', 'ocupacao', 'genero', 'telefone',
                  'cidade','estado', 'descricao']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
```

Na views vamos trabalhar com 2 formulário. Contas e Perfil do usuario.

apps/perfil/views.py

```python
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404, render, redirect
from contas.forms import UserChangeForm
from perfil.forms import PerfilForm
from perfil.models import Perfil

@login_required 
def editar_perfil(request, username):
    redirect_route = request.POST.get('redirect_route', '')
    modelo_myuser = MyUser.objects.get(username=username)
    modelo_perfil = Perfil.objects.get(usuario__username=username)
    message = 'Seu Perfil foi atualizado com sucesso!'
    if request.user.username != modelo_myuser.username and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
        return redirect('lista-postagem-forum')  # Adicionar uma rota "sem permissão"

    if request.method == 'POST':
        form_contas = UserChangeForm(request.POST, user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=modelo_perfil)
        if form_perfil.is_valid() and form_contas.is_valid():
            form_contas.save()
            form_perfil.save()
            messages.warning(request, message)
            return redirect(redirect_route)
    else:
        form_contas = UserChangeForm(user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(instance=modelo_perfil)

    context = {'form_perfil': form_perfil, 'form_contas': form_contas, 'obj': modelo_myuser}
    return render(request, 'editar-perfil-form.html', context)
```

apps/perfil/t/urls.py

```python
path('editar-perfil/<slug:username>/', editar_perfil, name='editar-perfil'),
```

apps/perfil/templates/editar-perfil-form.html

```python
{% extends "base_dashboard.html" %}
{% block title %}Editar Perdil{% endblock %}
{% load static %}
{% block content_dash %}
<div class="row"> 
    <div class="col-md-8">
        <form class="row p-3 rounded-3 shadow-sm" method="post" action="?" 
            enctype="multipart/form-data">
            {% csrf_token %}
            <h4>Editar Informações Pessoais</h4>
            <p>Perfil {{obj.username}}</p>
            <div class="col"> 
                {% if obj.perfil.foto %}
                <img src="{{obj.perfil.foto.url}}" class="img-fluid rounded" alt="{{obj.username}}" width="100">
                {% else %}
                <img src="{% static 'images/perfil/foto-padrao.jpg' %}" class="img-fluid rounded" width="100" alt="">
                {% endif %}  

                {{ form_perfil.as_p }}
            </div>
            <div class="col">
                <p>Informações da Conta do Usuário</p>
                {{ form_contas.as_p }}
            </div> 
            <div class="div">
                <input type="hidden" name="redirect_route" value="{{ request.path }}">
                <button type="submit" class="btn btn-primary">Salvar</button>
                <button type="button" class="btn btn-secondary">Cancelar</button>
            </div>
        </form>
    </div> 
</div> 
{% endblock %}
```

Vamos atualizar os botão para redirecionar para formulário.

apps/perfil/templates/perfil.html

```python
<a class="btn btn-warning" href="{% url 'editar-perfil' obj.username %}" role="button">
    <i class="fas fa-cog"></i> Editar Perfil
</a>
```

apps/contas/templates/lista-usuario.html

```html
<td scope="row">
	<a class="link-warning" href="{% url 'perfil' usuario.username %}"><i class="fas fa-eye mx-2"></i></a>
	<a class="ml-2 link-secondary" href="{% url 'editar-perfil' usuario.username %}"><i class="far fa-file mx-2"></i></a>
	<a class="ml-3 link-danger" href=""><i class="fas fa-trash mx-2"></i></a>
</td>
```

Configurações do Dashboard podemos adicionar uns atalhos.

apps/config/templates/configuracao.html
```python
<ul>
	  <li><a href="{% url 'atualizar_usuario' request.user.username %}">Alterar Configurações da Conta</a></li>
	  <li><a href="{% url 'password_change' %}">Alterar minha senha</a></li>
	  <li><a href="{% url 'editar-perfil' request.user.username %}">Editar meu Perfil</a></li> 
	  {% if perms.contas.view_myuser %}
	  <li><a href="{% url 'lista_usuarios' %}">Lista Todos usuários</a></li>
	  {% endif %} 
</ul>
```