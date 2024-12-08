## Formulário de Contato Via Ajax

### Backend - Configurar a View para Processar o Formulário

Crie uma view para processar o envio do formulário:

*apps/pages/views.py*

```python
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def enviar_contato(request):
    if request.method == "POST": # Pega os valores do formulário
        data = json.loads(request.body)
        nome = data.get('nome')
        email = data.get('email')
        titulo = data.get('titulo')
        mensagem = data.get('mensagem')

        if not all([nome, email, titulo, mensagem]): # Valida se todos estão preenchidos
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)

        try:
            send_mail( # Usa send_mail lib para enviar email
                f"Contato: {titulo}",
                f"Nome: {nome}\nE-mail: {email}\nMensagem: {mensagem}",
                'seu-email@dominio.com',  # Email de envio
                ['email-destino@dominio.com'],  # Email de destino
                fail_silently=False,
            )
            return JsonResponse({'message': 'Mensagem enviada com sucesso!'})
        except Exception as e:
            return JsonResponse({'error': f"Erro ao enviar mensagem: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)

```

Adicione essa view no `urls.py`:

```python
from django.urls import path
from .views import enviar_contato

urlpatterns = [
    path('enviar-contato/', enviar_contato, name='enviar_contato'),
]

```

---

### Configurar o Envio com AJAX

Atualize o formulário no template para capturar o evento `submit` e enviar os dados via AJAX:

*pages/componentes/contato.html*

```html
<form id="form-contato" class="row p-5 m-5 bg-light">
    <h4>Formulário de Contato</h4>
    <div class="form-group">
        <input type="text" id="nome" class="form-control" placeholder="Seu nome">
    </div>
    <div class="form-group">
        <input type="email" id="email" class="form-control" placeholder="Seu E-mail">
    </div>
    <div class="form-group">
        <input type="text" id="titulo" class="form-control" placeholder="Titulo">
    </div>
    <div class="form-group">
        <textarea id="mensagem" cols="30" rows="7" class="form-control" placeholder="Mensagem..."></textarea>
    </div>
    <div class="form-group">
        <input type="submit" value="Enviar Mensagem" class="btn btn-secondary py-3 px-5">
    </div>
</form>
<div id="resultado"></div> 
```

*apps/pages/index.html*

```jsx
{% block scripts %}
<script>
  document.getElementById('form-contato').addEventListener('submit', function (e) {
      e.preventDefault();

      const nome = document.getElementById('nome').value;
      const email = document.getElementById('email').value;
      const titulo = document.getElementById('titulo').value;
      const mensagem = document.getElementById('mensagem').value;

      fetch("{% url 'enviar_contato' %}", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": "{{ csrf_token }}",
          },
          body: JSON.stringify({ nome, email, titulo, mensagem }),
      })
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              document.getElementById('resultado').innerHTML = `<p class="text-danger">${data.error}</p>`;
          } else {
              document.getElementById('resultado').innerHTML = `<p class="text-success">${data.message}</p>`;
              document.getElementById('form-contato').reset();
          }
      })
      .catch(error => {
          document.getElementById('resultado').innerHTML = `<p class="text-danger">Erro ao enviar mensagem.</p>`;
      });
  });
</script> 
{% endblock scripts %} 
```

---

### Configuração de E-mail no Django

Certifique-se de configurar corretamente o envio de e-mails no arquivo `settings.py`:

```python
# Vamos utilizar email backend do django para simulação
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
```

*base/templates/base.html*

```jsx
 	... 
	{% include "components/scripts.html" %}

	{% block scripts %} {% endblock scripts %} Adiciona isso
</body>
</html>
```