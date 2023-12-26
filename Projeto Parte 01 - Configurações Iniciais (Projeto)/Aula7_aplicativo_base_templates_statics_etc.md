***Aplicativo Base (templates, statics)***

Dev: Letícia Lima

**Vamos criar nosso primeiro aplicativo base no Django.**

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

https://docs.djangoproject.com/pt-br/4.2/ref/templates/language/

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
	
	<!-- CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">	
	<link rel="stylesheet" href="{% static 'css/style.css' %}">
	
</head>
<body>
	{% block content %}{% endblock %}
	<!-- JS-->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>
 	<script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" integrity="sha384-rOA1PnstxnOBLzCLMcre8ybwbTmemjzdNlILg8O7z1lUkLXozs4DHonlDtnE7fpc" crossorigin="anonymous"></script>
	<script src="{% static 'js/scripts.js' %}"></script>
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