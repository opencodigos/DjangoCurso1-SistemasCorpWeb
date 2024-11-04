***Criando Aplicativo***

**Dev: Letícia Lima** 
    
**Vamos criar nosso aplicativo no Django Teste**

Para criar a aplicação no Django rode comando abaixo. “pages” é nome do seu **Aplicativo**.

```python
python manage.py startapp pages
```

Agora precisamos registrar nossa aplicação no *INSTALLED_APPS* localizado em *settings.py*.

pages/*templates*/*index.html*

```html
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}
    <h1>Pagina 1</h1> 
{% endblock %}
```

pages/*views.py*

```python
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
```

criar arquivo pages/*urls.py*

```
from django.urls import path 
from pages import views

urlpatterns = [
    path('', views.index, name='home'), 
]
```

core/settings.py

```python
PROJECT_APPS = [ 
    'apps.pages', 
]
```

urls.py do projeto. ***core/urls.py***

```python
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from base.views import base_view

urlpatterns = [
    path('admin/', admin.site.urls), ,
    path('base/', base_view, name='base'),
    
    path('', include('pages.urls')), # url do app 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Rodar o projeto para ver como está.

```python
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cda72dc9-de6c-49a6-8797-805a2966f9e4/Untitled.png)