# **Rota de Atualizar Usuário**

Dev: Letícia Lima

apps/contas/forms.py

```python
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name','is_active']
        help_texts = {'username': None}
        labels = {
            'email': 'Email', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario Ativo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
```

apps/contas/views.py

```python
from django.contrib.auth.decorators import login_required

@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'user_update.html', {'form': form})
```

apps/contas/templates/user_update.html

```python
{% extends 'base.html' %}
{% block title %}Formulário Alterar Usuário{% endblock %}
{% block content %}
<div class="row p-5 bg-light">
    <h3>Atualizar Usuário</h3>
    <form method="post">
        {% csrf_token %}
       {{form}}
       <div class="mt-3">
            <button type="submit" class="btn btn-primary mt-3">Alterar</button> 
       </div>
    </form>  
</div>
{% endblock %}
```

apps/contas/urls.py

```python
path('atualizar-usuario/', views.atualizar_meu_usuario, name='atualizar_meu_usuario'),
```

Nesse exemplo, a rota é definida para **`/usuario/<int:user_id>/atualizar/`**. O valor **`user_id`** é um parâmetro inteiro que será passado na URL. O nome da view é **`user_update`** e o nome da rota é **`user_update`**. Vamos aproveitar o mesmo template que usamos na outra rota para atualizar o usuário autenticado.

apps/contas/views.py

```python
from django.shortcuts import get_object_or_404
from contas.models import MyUser

@login_required()
def atualizar_usuario(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'user_update.html', {'form': form})
```

apps/contas/urls.py
```python
path('atualizar-usuario/<int:user_id>/', atualizar_usuario, name='atualizar_usuario'),
```