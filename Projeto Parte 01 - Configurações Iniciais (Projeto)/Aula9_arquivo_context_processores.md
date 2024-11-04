***Arquivo Context Processors***

**Dev: Letícia Lima** 
    
O **context_processors** é uma função no Django que processa dados de contexto para serem disponibilizados em todos os templates. 

Essa função pode ser personalizada pelo desenvolvedor para adicionar variáveis de contexto customizadas que serão acessíveis em todas as páginas renderizadas pelo servidor. Essa é uma forma eficiente de tornar dados globalmente disponíveis em todas as views e templates.

https://docs.djangoproject.com/pt-br/5.1/ref/templates/api/

Primeiro criar um arquivo ***context_processors.py*** na pasta do seu projeto.

**core/context_processors.py** ou **apps/base/context_processors.py** (pode colocar onde você quiser)

```python
# from pages import models

def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}
```

Ai precisamos registar as funções aqui.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR], # 03/11/2024 Adiciona variavel template_dir
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Apps
                'core.context_processors.context_social', 
            ],
        },
    },
]
```

Feito essa configuração o contexto “social” se torna Global no seu projeto. Assim você pode chamado em qualquer aplicativo do seu projeto.

pages/template/index.html

```python
{% extends 'base.html' %}
{% block title %}Pagina 1{% endblock %}
{% block content %}
    <h1>Pagina 1</h1>
    <p>Testando o context Global</p>
    <p>{{social}}</p>
{% endblock %}
```