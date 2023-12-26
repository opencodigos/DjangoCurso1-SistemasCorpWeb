# Gerenciador de Senhas

**Dev: Letícia Lima**

### Password Reset

Primeiro vamos fazer uma configuração no ***core/settings.py*** e adicionar o **EMAIL_BACKEND** do Django, para simular um envio de e-mail para reset de senha.

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

Documentação: 
https://docs.djangoproject.com/en/4.1/topics/auth/default/
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
https://docs.djangoproject.com/en/4.2/topics/auth/default/#module-django.contrib.auth.views

Vamos configurar a autenticação da maneira mais simples que conheço com Django.

Então com base na documentação, vamos praticamente importar rotas ***“accounts”***  

Primeiro vamos registrar essas urls no nosso projeto.

apps/contas/urls.py

```python
urlpatterns = [
		...
    path("", include("django.contrib.auth.urls")),  # Django auth
]
```

Isso inclui todos esses padrões de URL.

```
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
```

Com isso já conseguimos testar. Rode a aplicação e tenta acessar qualquer uma dessas rotas. http://localhost:8000/contas/password_change/

Cada comportamento dessas Urls ira redirecionar para admin do django. Isso por que está utilizando o **template da view padrão do accounts**.

Mas podemos criar nosso template e customizar, de maneira simples. 

Verifique no core/settings.py do seu processo se colocamos esses paramentros.

```python
# --- Login Logout User --- # 
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

**Primeiro Reset Password**

apps/contas/templates/registration/password_reset_form.html

Esse será nosso template customizado para essa rota. Estamos herdando o template de base_auth.html que criamos para esse tipo de autenticação.

```python
{% extends 'base_auth.html' %}
{% block title %}Resetar Senha{% endblock %}
{% block content_auth %}  
<form method="post">
    {% csrf_token %}
    <div class="mt-3">
        <label class="form-label" for="id_email">Entre com seu e-mail para resetar sua senha.</label>
        <input type="email" name="email" class="form-control" id="id_email">
    </div>
    <button class="btn btn-secondary mt-3" type="submit">Resetar</button>
</form> 
{% endblock %}
```

Se testarmos agora http://localhost:8000/contas/password_reset/ a rota está redirecionando para o admin do django. Isso por que estamos aproveirando a rota padrão dele. Então vai acontecer. Para que nosso projeto reconheça nosso template ao acessar essa rota, vamos precisar fazer uma modificação no core/settings.py do projeto. 

```python
DJANGO_APPS = [
    'apps.contas', # Adiciona 
    'django.contrib.admin',
		...
]

THIRD_APPS = [
    'corsheaders',
]

PROJECT_APPS = [
    'apps.base',
    # 'apps.contas', # Remover
    'apps.home',
]
```

Dessa forma inicia nosso app contas como primario e carregará nosso template customizado.

Uma segunda alternativa seria criar todas as views e forms e realizar todas as configurações necessárias. No entanto, no caso em questão, não foram aplicadas regras ou customizações extensas aos campos, como fizemos ao criar as views de login e registro. Essa abordagem é opcional e vocês podem escolher utilizá-la. Além disso, há outras maneiras de realizar essa tarefa, como descrito na documentação.

apps/contas/templates/login.html

```html
<span>Esqueceu sua senha? <a class="text-reset" href="{% url 'password_reset' %}">Resetar</a></span>
```

### **Password Reset Confirm**

Depois de Enviar o e-mail para resetar a senha. O usuário vai acessar a rota para digitar a nova senha. é esse template abaixo que vamos customizar.

apps/contas/templates/registration/password_reset_confirm.html

```python
{% extends 'base_auth.html' %}
{% block title %}Formulário Reset Senha{% endblock %}
{% block content_auth %} 
{% if validlink %}
<p>Entre com sua nova senha para resetar.</p>
<form action="" method="post">
    {% csrf_token %}
    <div class="mt-3">
        {{ form.new_password1.errors }}
        <label class="form-label" for="id_new_password1">Nova Senha:</label>
        <input type="password" name="new_password1" class="form-control" id="id_new_password1"> 
    </div>
    <div class="mt-3">
        {{ form.new_password2.errors }}
        <label class="form-label" for="id_new_password2">Confirmação de senha:</label>
        <input type="password" name="new_password2" class="form-control" id="id_new_password2"> 
    </div>
    <button type="submit" class="btn btn-secondary mt-3">Alterar Senha</button>
</form>
{% else %}
<h1>Falha na redefinição de senha</h1>
<p>O link de redefinição de senha era inválido, possivelmente porque já foi usado. Solicite uma nova redefinição de senha.</p>
{% endif %} 
{% endblock %}
```

### **Password Reset Complete**

Depois que digitar a nova senha vamos confirmar a mudança e usuário será redirecionado para essa rota. Segue template abaixo.

apps/contas/templates/registration/password_reset_complete.html

```html
{% extends 'base_auth.html' %}
{% block title %}Reset de Senha Completo{% endblock %}
{% block content_auth %} 
<div class="d-flex text-success">
    <i class="fas fa-check-circle fa-2x"></i>
		<h3>Sua senha foi alterada com sucesso!</h3>
</div>
<p><a href="{% url 'login' %}">Fazer Login</a></p> 
{% endblock %}
```

### **Password Reset Done**

apps/contas/templates/registration/password_reset_done.html

```python
{% extends 'base_auth.html' %}
{% block title %}Reset Ok{% endblock %}
{% block content_auth %} 
<h3>Solicitação de Senha Nova</h3>
<p>Enviamos um e-mail com instruções para definir sua senha. Se eles não chegarem em alguns minutos, verifique sua pasta de spam.</p>
{% endblock %}
```

### **Password Change**

Essa rota é quando sabemos a senha e queremos alterar. Lembrando que usuario precisa estar autenticado para acessar essa rota.

Primeiro eu vou criar um change_form.html onde vai ficar o formulário para mudança de senha. Depois vamos usar o include para incluir no template password_change.html

apps/contas/templates/registration/change_form.html

```html
<form action="" method="post">
    {% csrf_token %} 
    <div class="mt-3">
        {{ form.old_password.errors }}
        <label class="form-label" for="id_old_password">Senha Antiga:</label>
        <input type="password" name="old_password" class="form-control" id="id_old_password">
    </div>
   
    <div class="mt-3">
        {{ form.new_password1.errors }}
        <label class="form-label" for="id_new_password1">Nova Senha:</label>
        <input type="password" name="new_password1" class="form-control" id="id_new_password1">
    </div>

    <div class="mt-3">
        {{ form.new_password2.errors }}
        <label class="form-label" for="id_new_password2">Confirmação de senha:</label>
        <input type="password" name="new_password2" class="form-control" id="id_new_password2">
    </div>
    <button type="submit" class="btn btn-secondary mt-3">Alterar Senha</button>
</form>
```

Nota que mudamos para base.html estamos herdando o template base normal. Por que ? Não temos um dashboard ainda. E essa rota acontece quando usuário está autenticado. Então renderizo o formulário na pagina base inicial mesmo. (por enquando).

apps/contas/templates/registration/password_change_form.html

```python
{% extends 'base.html' %}
{% block title %}Formulário Reset Senha{% endblock %}
{% block content %}
 <div class="row p-5 bg-light m-5">
    <h3>Alterar Senha</h3>
    {% include "registration/change_form.html" %}
 </div>
{% endblock %}
```

**Por que estou fazendo isso, separando o form e incluindo depois no template**. Pensando no futuro vamos ter outro formulário de mudança de senha. que vamos implementar, vai ser o password_change_force.html onde vamos forçar o usuário no primeiro acesso a mudar a senha. **Mas isso vamos fazer mais pra frente. É bom já deixarmos adaptavel.**

Feito isso pode testar: http://localhost:8000/contas/password_change/ 

A rota está acessivel mas ainda falta configurar template de sucesso quando o formulário for valido e redirecionar para mensagem de sucesso.

### **Password Change Done**

apps/contas/templates/registration/password_change_done.html
```python
{% extends 'base.html' %}
{% block title %}Reset Ok{% endblock %}
{% block content %}
<div class="p-5 bg-light">
   <div class="d-flex align-items-center gap-3 link-success">
      <i class="fa fa-check fa-5x"></i>
      <h3>Sua senha foi alterada com sucesso!</h3>
   </div> 
</div>
{% endblock %}
```