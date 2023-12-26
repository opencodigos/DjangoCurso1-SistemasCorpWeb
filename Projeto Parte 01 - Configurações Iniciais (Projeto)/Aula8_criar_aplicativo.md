***Criando Aplicativo***

**Dev: Letícia Lima**

**Vamos criar nosso aplicativo no Django Teste**

Para criar a aplicação no Django rode comando abaixo. “myapp” é nome do seu **Aplicativo**.

```python
python manage.py startapp pages
```

Agora precisamos registrar nossa aplicação no *INSTALLED_APPS* localizado em *settings.py*.

*myapp*/*templates*/*index.html*

```html
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}
	<h1>Pagina 1</h1>
	<p>Testando o context Global</p>
	<p>{{social}}</p>
{% endblock %}
```

*myapp*/*views.py*

```python
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
```

criar arquivo *myapp*/*urls.py*

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
from django.urls import path, include # adicionar include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')), # url do app
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto
```

Rodar o projeto para ver como está.

```python
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```
 