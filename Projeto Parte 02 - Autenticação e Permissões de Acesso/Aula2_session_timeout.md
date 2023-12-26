# **Rota Session Timeout**

**Dev: Letícia Lima**

O django-session-timeout é uma biblioteca que adiciona funcionalidade de expiração automática de sessões de usuário inativas em projetos Django.
Com essa biblioteca, é possível definir o tempo limite de inatividade para expirar a sessão, além de poder personalizar a mensagem de aviso de expiração.

**Para usá-la, basta instalar a biblioteca via pip e adicionar a configuração no arquivo de configuração do Django.** 

doc: https://pypi.org/project/django-session-timeout/

**`pip install django-session-timeout`**

```python
MIDDLEWARE_CLASSES = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    # ...
]
```

```python
# timeout tempo de inatividate no sistema
SESSION_EXPIRE_SECONDS = 1800 
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60  
SESSION_TIMEOUT_REDIRECT = 'http://localhost:8000/'
```

**`SESSION_EXPIRE_SECONDS`** tempo em segundos até que a sessão expire por inatividade;

**`SESSION_EXPIRE_AFTER_LAST_ACTIVITY`** indica se a sessão deve expirar após o último acesso do usuário (ou seja, se a sessão deve ser renovada a cada requisição)

**`SESSION_TIMEOUT_REDIRECT`** URL para redirecionar o usuário quando a sessão expirar. Nesse caso, estamos redirecionando para **`http://localhost:8000/`**

`**SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD**` especifica um período de carência (em segundos) para o tempo limite de expiração da sessão, ou seja, se um usuário fizer uma ação antes do período de carência expirar, o tempo limite será renovado e a sessão não será expirada.

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

Vamos criar a view para exibir mensagem para usuario que foi desconectado por inatividade.

```python
def timeout_view(request):
    return render(request, 'timeout.html')
```

```python
path('timeout/',  views.timeout_view, name='timeout'),
```

apps/contas/templates/timeout.html

```html
{% extends "base.html" %}
{% block content %} 
<div class="container">
    <div class="row align-items-center justify-content-center">
        <div class="col-md-4">
            <h3>Você foi desconectado do sistema por inatividade</h3>
        </div>
    </div>
</div>
{% endblock %}
```

e no settings atualizar a rota de redirecionamento.

`SESSION_TIMEOUT_REDIRECT = 'http://localhost:8000/contas/desconectado-inatividade/'`