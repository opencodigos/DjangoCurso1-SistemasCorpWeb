# **Rota de Login**

**Dev: Letícia Lima**

apps/contas/views.py

```python
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')
```

apps/contas/urls.py

```python
from django.urls import path
from contas import views 

urlpatterns = [
    path('entrar/', views.login_view, name='login'), 
]
```

apps/contas/templates/login.html

```html
{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %} 
<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <h4>Login</h4>
    <div class="mt-3">
        <label for="email">Email:</label>
        <input type="email" name="email" class="form-control" required>
    </div>  
    <div class="mt-3">
        <label for="password">Senha:</label>
        <input type="password" name="password" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary mt-3">Entrar</button>
    <div class="mt-3">
        <span>Ainda não tem conta? <a class="text-reset" href="#">Cadastre-se</a></span><br>
        <span>Esqueceu sua senha? <a class="text-reset" href="#">Resetar</a></span>
    </div>  
</form>   
{% endblock %}
```

core/urls.py

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('contas.urls')), # Adiciona contas
    path('', include('pages.urls')),
]
```

No index.html do aplicativo “pages’ podemos adicionar essa tag para verificar se login foi feito.

```html
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}
	<div class="container mt-3">

		{% if user.is_authenticated %} # Adiciona 
		<h4>Olá {{user.first_name}} {{user.last_name}}, </h4>
		<h6>Bem Vindo(a)</h6>
		{% endif %} 

		<p>Pagina 1</p>
		<p>Testando o context Global</p>
		<p>{{social}}</p>
	</div>
{% endblock %}
```

### **Vamos customizar um pouco essa parte de autenticação.**

Como combinamos no inicio vamos utilizar bootstrap/CSS para layout da pagina.

No django podemos criar um template base e depois criar um outro template base_auth para herdar a base. Como no exemplo abaixo.

Vou usar esse template base somente para rotas de autenticação, então criei ele em:

**apps/base/templates/base_auth.html**

```python
{% extends 'base.html' %}
{% block title %}Autenticação{% endblock %}
{% block content %} 
<div class="container col-xl-10 col-xxl-8 px-4 py-5">
    <div class="row g-lg-5 py-5">
        <div class="col-lg-7"></div>
        <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5 rounded-4 bg-light shadow-sm">
            {% include 'components/messages.html' %}
            {% block content_auth %}{% endblock %}
            <div class="text-muted py-4">
                <small>Copyright© 2023 Name</small>
            </div>
        </div>
    </div>
</div> 
{% endblock %}
```

**apps/contas/login.html** - atualizando fica assim

```python
{% extends 'base_auth.html' %}
{% block title %}Login{% endblock %}
{% block content_auth %}
<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <h4>Login</h4>
    <div class="mt-3">
        <label for="email">Email:</label>
        <input type="email" name="email" class="form-control" required>
    </div>  
    <div class="mt-3">
        <label for="password">Senha:</label>
        <input type="password" name="password" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary mt-3">Entrar</button>
    <div class="mt-3">
        <span>Ainda não tem conta? <a class="text-reset" href="#">Cadastre-se</a></span><br>
        <span>Esqueceu sua senha? <a class="text-reset" href="#">Resetar</a></span>
    </div>  
</form>   
{% endblock %}
```

**Feito isso o resultado bem bonito.**