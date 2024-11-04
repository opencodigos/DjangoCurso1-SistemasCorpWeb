***Aplicativo Base (templates, statics)***

Dev: Letícia Lima 
    
## **Vamos criar nosso primeiro aplicativo base no Django.**

Aplicação ***base*** vamos deixar os arquivos base que é utilizado no projeto inteiro. Como **templates padrão** e **arquivos statics** como **css, js, images estáticas, font, icone**. Coloca as coisas que você não vai mudar ao longo do tempo. 

Se seu projeto for uma aplicação dinâmica que esses arquivos precisam ser alterados por um administrador. É mais relevante criar um app “**Config**” e configurar um modelo para fazer esses tipos de configuração.
**Podemos fazer um exemplo disso depois.**  

Bom vamos lá, Criar a aplicação base. Lembre que vamos colocar essa aplicação dentro da pasta “apps”.

```python
python manage.py startapp base
```

Agora precisamos registrar nossa aplicação no *PROJECT_APPS*  localizado em *settings.py*.

```python
...
PROJECT_APPS = [
	'apps.base', # Adiciona app base aqui
]
...
```

Apos criar app base pode criar as pastas nessa estrutura.   

**Estrutura tem que ficar assim:**

```python
site_sistema/
├── apps/
│   ├── **base**/
│   │   ├── migrations/
│   │   ├── **static**/
│   │   │   ├── **css**/
│   │   │   ├── **js**/
│   │   │   ├── **fonts**/
│   │   │   └── **images**/
│   │   ├── **templates**/
│   │   └── __init__.py 
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── **context_processors.py**
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Template Base

Vamos criar um template base para nossa paginas iniciais do projeto. 

É aqui que vamos renderizar nosso conteúdo. Para não ter que repetir esse template em todas as paginas que criarmos, então fazemos um base e utilizamos *extends* para usar nos outros templates. 

https://docs.djangoproject.com/pt-br/5.1/ref/templates/language/

*base/templates/base.html*

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
	
	<!-- CSS Boostrap, style -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	<link rel="stylesheet" href="{% static 'css/style.css' %}">
	
</head>
<body>
	{% block content %}{% endblock %}

	<!-- JS bootstrap, jquery, script-->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script> 	<script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" integrity="sha384-rOA1PnstxnOBLzCLMcre8ybwbTmemjzdNlILg8O7z1lUkLXozs4DHonlDtnE7fpc" crossorigin="anonymous"></script>
	<script src="{% static 'js/script.js' %}"></script>
	{% block scripts %}{% endblock scripts %}
</body>
</html>
```

**Link do JQUERY**: [https://releases.jquery.com](https://releases.jquery.com/)

**Link Font Awesome** : [https://fontawesome.com](https://fontawesome.com/) ou https://fontawesome.com/v5/docs/web/use-with/python-and-django ou https://fontawesome.com/v5/docs/web/use-with/wordpress/install-manually

**Os metas tags que podemos já deixar configurado, depois….** 
Para vocês saberam mais sobre isso, da uma pesquisa sobre **SEO, paginas de alto nivel, mecanismo de pesquisa. (não manjo muito)**

```html
<meta name="description" content="Descrição do conteúdo do site">
usado para fornecer uma breve descrição do conteúdo do site que pode ser usado pelos mecanismos de pesquisa.

<meta name="keywords" content="palavras-chave separadas por vírgula"> 
usado para fornecer palavras-chave relevantes para o conteúdo do site que podem ser usadas pelos mecanismos de pesquisa.

<meta name="author" content="Nome do autor">
usado para especificar o nome do autor do site.

<meta name="robots" content="noindex, nofollow">
usado para instruir os mecanismos de pesquisa a não indexar ou seguir as páginas do site.

<meta property="og:title" content="Título compartilhado nas redes sociais">
usado para fornecer um título personalizado para ser usado quando o conteúdo do site é compartilhado em redes sociais.

<meta property="og:description" content="Descrição compartilhada nas redes sociais">
usado para fornecer uma descrição personalizada para ser usada quando o conteúdo do site é compartilhado em redes sociais.

<meta property="og:image" content="URL da imagem compartilhada nas redes sociais">
usado para fornecer uma imagem personalizada para ser usada quando o conteúdo do site é compartilhado em redes sociais.
```

Teste

base/views.py

```python
from django.shortcuts import render

# Create your views here.  
def base_view(request):
	return render(request, 'template.html')

```

base/templates/template.html

```html
{% extends "base.html" %}

{% block title %}My Amazing blog{% endblock %}

{% block content %}
<h1>Template Filho</h1> 
{% endblock %} 

{% block scripts %} 
{% endblock scripts %}
```

core/urls.py

```python
from base.views import base_view

urlpatterns = [ 
	path('base/', base_view, name='base'),
]
```