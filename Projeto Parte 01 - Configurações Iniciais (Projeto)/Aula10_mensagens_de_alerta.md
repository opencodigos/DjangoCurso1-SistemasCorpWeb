***Django Messages***

**Dev: Letícia Lima** 

**Configura mensagem.**

Documentação: https://docs.djangoproject.com/en/4.1/ref/contrib/messages/

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7313211f-5540-4cf8-9a58-8aa5d6b87718/Untitled.png)

Nossa biblioteca tem essas configurações de mensagens ativas. Que funciona perfeitamente, mas precisamos renderizar isso no *frontend*. Como estamos utilizando *bootstrap* precisamos adicionar essa configuração no *settings.py* do seu projeto. Adicionando essa configuração as mensagens de alerta aparecerá com as classes do bootstrap.

***core/settings.py***

```python
# Configuração de Messages (Class Boostrap) #
from django.contrib.messages import constants

MESSAGE_TAGS = {
	constants.ERROR: 'alert-danger',
	constants.WARNING: 'alert-warning',
	constants.DEBUG: 'alert-danger',
	constants.SUCCESS: 'alert-success',
	constants.INFO: 'alert-info',
}
```

Criei uma pasta **components** e dentro vou colocar os components que podem ser reutilizados em varias paginas.
***base/templates/components/message.html***

```python
{% if messages %}
<div class="messages">
	{% for message in messages %}
	<div class="alert {{ message.tags }} alert-dismissible fade show" role="alert">
		{{ message }}
		<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
	</div>
	{% endfor %}
</div>
{% endif %}
```

**Adiciona na base**

base/templates/base.html

```python
...
<body> 
	{% include 'components/message.html' %} <!-- ## adiciona isso. -->
	{% block content %}{% endblock %} 
</body>
...
```

**testar** 

pages/views.py

```jsx
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def index(request):
	messages.success(request, "Operação realizada com sucesso!")
	messages.error(request, "Ocorreu um erro!")
	messages.warning(request, "Atenção com esta ação.")
	messages.info(request, "Essa é uma informação.")
	return render(request, 'index.html')
```