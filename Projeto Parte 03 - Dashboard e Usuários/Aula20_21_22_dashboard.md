# **Dashboard**

**Dev: Letícia Lima**

Criamos algumas rotas de acesso porem visualmente está muito ruim de acessar. Então vamos montar um dashboard simples para ter as rotas de configuração e centralizar tudo ali.

**De inicio vai ser um dashboard simples certo ? já tenho um modelo pronto, feito com bootstrap e css.**

Nosso arquivo Base do dashboard será esse. Não vamos herda de base. Por que muda algumas coisas como navbar, sidebar, footer. Então achei melhor criar um arquivo base novo. Depois mais pra frente podemos fatorar algumas coisas, como por exemplo o head que é igual para todos e scritps.

apps/base/templates/base_dashboard.html

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="Descrição do conteúdo do site">
	<meta name="keywords" content="palavras-chave separadas por vírgula"> 
	<meta name="author" content="Nome do autor"> 
	<title>{% block title %}{% endblock %}</title>
	
	<!-- CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" 
	rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">	
	
	<link rel="stylesheet" href="{% static 'css/style.css' %}">

    <!-- Font Awesome -->
	<script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" 
	integrity="sha384-rOA1PnstxnOBLzCLMcre8ybwbTmemjzdNlILg8O7z1lUkLXozs4DHonlDtnE7fpc" crossorigin="anonymous"></script>

</head> 
<body> 
    {% include "components/logout.html" %}
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-secondary fixed-top" style="height: 70px">
        <div class="container-fluid"> 
            <a class="navbar-brand mx-5" href="/">
                <img src="{% static 'images/d-logo.png' %}" width="130" alt="" loading="lazy"/>
            </a>
            <a class="navbar-toggler border-0" data-bs-toggle="collapse" 
									data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" 
									aria-expanded="false" aria-label="Toggle navigation">
                <i class="link-light fas fa-align-left fa-2x me-3"></i> 
            </a>
            <div class="navbar-nav ms-auto d-flex flex-row">
                <a class="link-light p-2" href="{% url 'perfil' user.username %}">
                    <i class="fas fa-user mx-2"></i>{{user.first_name}} {{user.last_name}}
                </a>
                <button class="btn btn-danger" data-bs-toggle="modal" href="#logoutModal">Logout</button>
            </div>
        </div> 
    </nav>

    <!-- Sidebar -->
    <div id="sidebarMenu" class="collapse d-lg-block sidebar collapse bg-secondary">
        <div class="list-group gap-2">
            <button type="button" class="btn btn-warning active" aria-current="true" onclick="location.href='{% url 'home' %}'">
								<i class="fas fa-arrow-left me-2"></i>Site</button>
            <button type="button" class="btn btn-light" aria-current="true"><i class="fas fa-tachometer-alt me-2"></i>Painel</button>
            <button type="button" class="btn btn-light"><i class="fas fa-file-alt me-2"></i>Relatórios</button>
            <button type="button" class="btn btn-light"><i class="fas fa-users me-2"></i>Usuários do Sistema</button>
            <button type="button" class="btn btn-light"><i class="fas fa-cog me-2"></i>Configurações</button>
        </div>
    </div>

    <!-- Container -->
    <div class="bloco"> 
        {% include 'components/messages.html' %} 
        {% block content_dash %} 
        {% endblock %}   
    </div>

    <footer class="nav-bottom py-2 bg-light mt-auto fixed-bottom">
        <div class="container-fluid px-4 mt-auto">
            <div class="d-flex align-items-center justify-content-between">
                <div class="text-muted">
                    <a>Core</a>
                </div>
                <div class="text-muted">
                    <a>Release 1.0.0 <br> Patch 01</a>
                </div>
                <a class="text-muted">2023 Copyright &copy; Nome</a>
                <div>
                    <a class="text-muted" href="#">Politica de Privacidade</a>
                    &middot;
                    <a class="text-muted" href="#">Termos &amp; de condições</a>
                </div>
            </div>
        </div>
    </footer>

	<!-- JS-->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" 
	integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.6.4.min.js" 
	integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>
	<script src="{% static 'js/scripts.js' %}"></script>
</body>
</html>
```

apps/base/static/css/global.css

```css
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Open+Sans&family=Roboto:wght@400;500;900&display=swap');

:root {
	--main-color-default: #5c5b5b;
	--main-color: #fbf8f8;
	--color-dark: #171515;
	--color-success: #05c318;
	--color-danger: #c50000;
	--color-warning: #efd400;
	--color-disable: #a3a3a3;
	--button-hover: #797979;
}

/* Site Configuration */
body {
	width: 100%;
	height: 100%;
	overflow-x: hidden;
	font-family: 'Roboto', sans-serif;
}

a {
	text-decoration: none;
	color: var(--color-disable);
}
```

apps/base/static/css/style.css

```css
@import url('global.css');

.sidebar {
    position: fixed;
    height: 100%;
    padding: 10px 15px 0;
    z-index: 0;
}

.sidebar button {
    height: 60px;
}

.bloco {
    margin: 70px 0px 70px 0px;
}

.pagination .page-link {
    background: rgb(138, 138, 138);
    color: white;
    border: none;
}

@media (min-width: 968px) {
    .bloco {
        padding-left: 250px;
    }

    /* .collapse:not(.show) {
        display: flex;
    } */
}

@media (max-width: 968px) {
    .sidebar {
        width: 100%;
    }

    .navbar-brand {
        display: none;
    }

    footer {
        display: none;
    }
}
```

Só isso não precisa fazer mais nada. Você terá um dashboard simples muito bonito.

---

### **O que podemos enviar nosso template para ser renderizado no dashboard ?**

Por enquando é essas duas. 

`**password_change_form.html**`

`**password_change_done.html**`

Podemos mudar o extends para base_dashboard.html

`**{% extends 'base_dashboard.html' %}**`

`**{% block content_dash %}**`

http://localhost:8000/contas/usuario/1/atualizar/

Vamos criar uma rota simples de configuração assim quando clicar em alterar minha senha abre a janela que precisamos.

Pensando em “configuração” podemos ter uma definição simples que será tudo aquilo que vamos configurar no nosso sistema e dados pessoais. 

Criaremos outro app separado somente para isso. 

```css
python manage.py startapp config
```

Registra no core/settings.py **PROJECT_APPS**

`**'apps.config'**`

Agora vamos criar uma view para quando usuario clicar em “Painel”.

apps/config/views.py

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def painel_view(request):
    return render(request, 'painel.html')
```

apps/config/urls.py

```python
from django.urls import path 
from config import views

urlpatterns = [
    path('', views.painel_view, name='painel'), 
]
```

apps/config/templates/painel.html

```html
{% extends 'base_dashboard.html' %}
{% block title %}Painel{% endblock %}
{% block content_dash %} 
<div class="p-5 bg-light">
	<h4>Bem-Vindo(a), {{user.first_name}} {{user.last_name}}</h4>
	<p>Painel administrativo do usuário.</p>
</div>
{% endblock %}
```

Em core/urls.py precisamos registrar a url do nosso app config.

`**path('config/', include('config.urls')),**`

No template base do Dashboard onde está a sidebar, configuramos o href do link.

`**onclick="location.href='{% url 'painel' %}'"**`

```html
<button type="button" class="btn btn-light" aria-current="true" onclick="location.href='{% url 'painel' %}'">
                <i class="fas fa-tachometer-alt me-2"></i>Painel</button>
```

Se acessarmos a rota: http://localhost:8000/config/

Vamos colocar um botão na home para enviar o usuário para dashboard. Lembrando que usuario precisa está autenticado para acessar o dashboard. Então na navbar colocar dentro da condição

`**if user.is_authenticated**`

apps/base/components/navbar.html 

```html
...
<button class="btn btn-warning mx-2" type="submit"  onclick="location.href='{% url 'painel' %}'">
                <i class="fas fa-cog"></i></button>
...
```

Com base nisso já temos um resultado legal.

### Agora rota “configuração”.

apps/config/views.py

```python
@login_required
def configuracao_view(request):
    return render(request, 'configuracao.html')
```

apps/config/urls.py

```python
urlpatterns = [
    ...
    path('configuracao/', views.configuracao_view, name='configuracao'),  
]
```

apps/config/templates/configuracao.html

```html
{% extends 'base_dashboard.html' %}
{% block title %}Configurações{% endblock %}
{% block content_dash %}

<div class="d-flex flex-wrap gap-3">
    <div class="p-5 bg-light" style="width: 430px;">
        <h4>Contas</h4>
        <p>Configurações do aplicativo contas</p>
        <ul>
            <li><a href="{% url 'password_change' %}">Alterar minha senha</a></li>
        </ul>
    </div>

    <div class="p-5 bg-light" style="width: 430px;">
        <h4>Sistema</h4>
        <p>Configurações de logo,Banner,informações empresa.</p>
        <ul>
            <li><a href="#">Alterar Informações da empresa</a></li>
            <li><a href="#">Alterar Banner Inicial</a></li>
            <li><a href="#">Tags/Metas/Robot</a></li>
            <li><a href="#">Alterar Logo</a></li>
        </ul>
    </div>
</div>

{% endblock %}
```

base/templates/base_dashboard.html

```html
<button type="button" class="btn btn-light" onclick="location.href='{% url 'configuracao' %}'">
                <i class="fas fa-cog me-2"></i>Configurações</button>
```

Bem legal neh. Bom já temos uma boa parte da estrutura do codigo pronta.