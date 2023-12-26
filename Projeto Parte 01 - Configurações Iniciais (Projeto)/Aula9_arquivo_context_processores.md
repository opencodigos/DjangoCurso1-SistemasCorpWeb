***Arquivo Context Processors***

**Dev: Letícia Lima**

O context_processors é uma função no Django que processa dados de contexto para serem disponibilizados em todos os templates. 

Essa função pode ser personalizada pelo desenvolvedor para adicionar variáveis de contexto customizadas que serão acessíveis em todas as páginas renderizadas pelo servidor. Essa é uma forma eficiente de tornar dados globalmente disponíveis em todas as views e templates.

https://docs.djangoproject.com/en/4.2/ref/templates/api/

Primeiro criar um arquivo ***context_processors.py*** na pasta do seu projeto.

**core/context_processors.py** ou **apps/base/context_processors.py** (pode colocar onde você quiser)

```python
# from myapp import models

def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}
```

Ai precisamos registar as funções aqui.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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