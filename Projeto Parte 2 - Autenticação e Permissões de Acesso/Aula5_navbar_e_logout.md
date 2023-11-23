# **Navbar e Logout**

**Dev: Letícia Lima**

Vamos configrar a navbar e os botões de **login/logout.** E aplicar algumas regras. Assim começamos a dar vida no sistema.

Com base na documentação estou utilizando primeiro exemplo de navbar que tem.

Documentação: https://getbootstrap.com/docs/5.3/components/navbar/#how-it-works

apps/base/templates/components/navbar.html

```html
<nav class="navbar navbar-expand-lg bg-light" style="height: 70px;">
    <div class="container-fluid bg-light">
        <a class="navbar-brand" href="/">EmpresaABC</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="#">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Sobre</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">FAQ</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Contato</a>
                </li>
            </ul>
            <form class="d-flex" role="search">
                <input class="form-control me-2" type="search" placeholder="Pesquisar" aria-label="Search">
                <button class="btn btn-success" type="submit">Pesquisar</button>
            </form>
        </div>
    </div>
</nav>
```

apps/base/templates/base.html

```html
<body>
	... 
	{% include 'components/navbar.html' %} 
	{% block content %}{% endblock %} 
	...
</body>
```

Quando subir o servidor a navbar já vai está aplicada. 

Agora vamos adicionar o botão de login e cadastro.

Para isso adicione o codigo abaixo. Veja que agora tem 2 botões um de login outro leva para rota cadastro que criamos posteriormente. 

A tag `onclick="location.href='{% url 'name' %}’` onde tem ‘name’ a gente coloca o nome da rota que está em urls do aplicativo para dizer aonde tem que ir quando usuário clicar no botão. Se fore uma tag de link ficaria assim `<a hrfe=”{% url 'name' %}”>` 

```html
...
<form class="d-flex" role="search">
	<input class="form-control me-2" type="search" placeholder="Pesquisar" aria-label="Search">
	<button class="btn btn-secondary" type="submit"><i class="fas fa-search"></i></button>
</form>
<button class="btn btn-primary mx-2" onclick="location.href='{% url 'login' %}'">Entrar</button>
<button class="btn btn-warning" onclick="location.href='{% url 'register' %}'">Cadastrar-se</button>
...
```

com base nisso vamos criar uma regra no template para quando usuario autentificado aparece um botão de logout. Mas antes precisamos criar a rota de logout.

apps/contas/

```python
# views.py
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')

# urls.py
path('sair/', views.logout_view, name='logout'),

# Criamos um botão assim para fazer logout
<button class="btn btn-danger" onclick="location.href='{% url 'logout' %}'">Logout</button>
```

Pode ver essa documentação sobre: https://docs.djangoproject.com/en/4.2/topics/auth/default/#all-authentication-views

atualizando o template apps/base/templates/components/navbar.html

```html
...
{% if user.is_authenticated %}
<span class="p-2"><i class="fas fa-user mx-2"></i>{{user.first_name}} {{user.last_name}}</span>
<button class="btn btn-danger" onclick="location.href='{% url 'logout' %}'">Logout</button>
{% else %}
<button class="btn btn-primary mx-2" onclick="location.href='{% url 'login' %}'">Entrar</button>
<button class="btn btn-warning" onclick="location.href='{% url 'register' %}'">Cadastrar-se</button>
{% endif %}
...
```

Vamos adicionar um popup para perguntar para usuário se ele gostaria de sair do sistema. Para isso vamos adicionar um novo componente chamado logout.

apps/base/templates/components/logout.html

```python
<div class="modal fade" id="logoutModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="logoutModalLabel">Atenção Usuario ! <i
						class="link-danger fas fa-exclamation-triangle me-2"></i></h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				Tem certeza que deseja sair do sistema ? <br>
				Após clicar em "Sair" você será deslogado.
			</div>
			<div class="modal-footer">
				<button class="btn btn-danger" onclick="location.href='{% url 'logout' %}'"><a>Sair</a></button>
			</div>
		</div>
	</div>
</div>
```

apps/base/templates/components/navbar.html

```python
<button class="btn btn-danger" data-bs-toggle="modal" href="#logoutModal">Logout</button>
```

apps/base/templates/base.html
```python
{% include 'components/logout.html' %}
```