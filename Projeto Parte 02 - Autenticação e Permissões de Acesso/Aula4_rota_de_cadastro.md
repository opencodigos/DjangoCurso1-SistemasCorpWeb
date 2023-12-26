# **Rota de Cadastro**

**Dev: Letícia Lima**

Na parte de cadastro vamos configurar o forms.py para criar o formulário de cadastro de cliente na plataforma.

apps/contas/forms.py

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from contas.models import MyUser 

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput) 
    password2 = forms.CharField(label="Confirmação de Senha", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'Email', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario Ativo?'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Senha não estão iguais!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
```

apps/contas/views.py

```python
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm()
    return render(request, "registration/register.html",{"form": form})
```

apps/contas/templates/register.html

```python
{% extends 'base_auth.html' %}
{% block title %}Login{% endblock %}
{% block content_auth %}
<form class="row" method="post" action="{% url 'register' %}">
    {% csrf_token %}
    <h4>Criar uma conta</h4> 
		 {{ form}}
    <button class="btn btn-primary mt-3" type="submit">Registrar</button>
    <div class="mt-3">
        <span><a class="text-reset" href="{% url 'login' %}">Fazer Login</a></span>
    </div>  
</form>  
{% endblock %}
```

apps/contas/urls.py

```python
urlpatterns = [
    path('entrar/', views.login_view, name='login'), 
    path('criar-conta/', views.register_view, name='register'), 
]
```

para ajudar os campos no template podemos fazer essa modificação.

```html
{% for field in form %}
  {% if field == form.email %}
  <div class="col-md-12">
      <div class="mt-3">
      {{ field.label_tag }}
      {{ field }}
      </div>
  </div>
  {% endif %}
  {% if not field == form.email %}
  <div class="col-md-6">
      <div class="mt-3">
      {{ field.label_tag }}
      {{ field }}
      </div>
  </div>
  {% endif %}
  {% endfor %}
```

Criar um usuário e adicionar o mesmo no grupo de usuário tipo padrão. Para que o mesmo tenha acesso ao perfil e possa criar as postagens.

```python
from django.contrib.auth.models import Group, User 

def register_view(request):
    ...
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
		...
```

No final fica assim 

```python
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()
            
            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm()
    return render(request, "registration/register.html",{"form": form})
```

apps/contas/templates/login.html
```html
<span>Ainda não tem conta? <a class="text-reset" href="{% url 'register' %}">Cadastre-se</a></span><br>
```