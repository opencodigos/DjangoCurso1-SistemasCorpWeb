# **Adicionar novo usuário**

Através do dashboard se um usuário administrador quiser adicionar um novo usuario no sistema. Vamos criar um formuário completo. 

Usaremos o modelo **MyUser** e **Perfil** juntar esses 2 formulários. Poderiamos usar a mesma função “register_view” mas para evitar modificações vamos criar uma nova separada.

**Primeiro precisamos criar o formulário do modelo Perfil que não existe ainda.**

apps/perfil/forms.py

```python
from django import forms
from perfil.models import Perfil
    
class PerfilForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=200
    )
    class Meta:
        model = Perfil
        fields = ['foto', 'ocupacao', 'genero', 'telefone',
                  'cidade','estado', 'descricao']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
```

apps/contas/views.py 

```python
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def adicionar_usuario(request):
    user_form = CustomUserCreationForm()
    perfil_form = PerfilForm()

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        perfil_form = PerfilForm(request.POST, request.FILES)

        if user_form.is_valid() and perfil_form.is_valid():
            # Salve o usuário
            usuario = user_form.save()

            # Crie um novo perfil para o usuário
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
 
            messages.success(request, 'Usuário adicionado com sucesso.')
            return redirect('lista_usuarios')

    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, "adicionar-usuario.html", context)
```

apps/contas/urls.py

```python
path('adicionar-usuario/',  views.adicionar_usuario, name='adicionar_usuario'),
```

apps/contas/templates/lista-usuarios.html

```python
<button class="btn btn-secondary" onclick="window.location.href='{% url 'adicionar_usuario' %}'">
			<i class="fas fa-user mx-2"></i> Adicionar Novo</button>
```

apps/contas/templates/adicionar-usuario.html

```python
{% extends 'base_dashboard.html' %}
{% block title %}Adicionar Usuário{% endblock %}
{% block content_dash %}
<div class="p-5 bg-light">
    <form class="row" method="POST" autocomplete="off" enctype="multipart/form-data">
        {% csrf_token %}
        <h4>Dados Conta Usuário (Principal)</h4>
        {{ user_form }}
	      {{ perfil_form }}
        <div class="mt-3">
            <button class="btn btn-primary mt-3" type="submit">Criar</button>
        </div>  
    </form>  
</div>
{% endblock %}
```

Vamos deixar os campos apresentado melhor no template. Depois essa parte voces podem customizar como quiser.

```python
{% extends 'base_dashboard.html' %}
{% block title %}Adicionar Usuário{% endblock %}
{% block content_dash %}
<div class="p-5 bg-light">
    <form class="row" method="POST" autocomplete="off" enctype="multipart/form-data">
        {% csrf_token %}
        <h4>Dados Conta Usuário (Principal)</h4>
        {% for field in user_form %}
        {% if field == user_form.email %}
        <div class="col-md-12">
            <div class="mt-3">
            {{ field.label_tag }}
            {{ field }}
            </div>
        </div>
        {% endif %}
        {% if not field == user_form.email %}
        <div class="col-md-6">
            <div class="mt-3">
            {{ field.label_tag }}
            {{ field }}
            </div>
        </div>
        {% endif %}
        {% endfor %} 

        <div class="mt-5">
            <h4>Dados Usuário (Perfil)</h4>
        </div>
        {% for field in perfil_form %} 
        <div class="col-md-6">
            <div class="mt-3">
            {{ field.label_tag }}
            {{ field }}
            </div>
        </div>
        {% endfor %} 

        <div class="mt-3">
            <button class="btn btn-primary mt-3" type="submit">Criar</button>
        </div>  
    </form>  
</div>
{% endblock %}
```

### **Campo Password ?**

<aside>
⛔ **Como podem perceber o campo senha aparece no formulario. Não ta errado por que no forms esse campo está lá para ser exibido pois utilizamos esse forms na tela de cadastro de usuario no inicio. Bom, como podemos aplicar uma regra ai. Pensei em algo simples de inicio. Se quando o administrador ou colaborador cadastrar um usuario no sistema, a gente enviar uma senha provisorio por e-mail ? Isso não seria legal ?**

</aside>

**Bom vamos fazer isso agora então.**

Pessoal primeiro passo é ocultar o campo senha do formulário somente quando acessar a rota de adicionar usuário. Isso acontece quando estamos autenticado certo ? No forms do app contas vamos fazer algumas modificações.

apps/contas/forms.py

```python
# class vamos fazer essa modificação
class CustomUserCreationForm(forms.ModelForm):
...
```

Usar **`CustomUserCreationForm(UserCreationForm)`** significa que você pode aproveitar as funcionalidades já definidas em **`UserCreationForm`**, como a validação de senhas e outros campos, mas você terá que seguir a estrutura do formulário definida nessa classe.

Já com **`CustomUserCreationForm(forms.ModelForm)`**, você pode definir os campos e as validações do formulário de acordo com as suas necessidades, sem se preocupar com a estrutura definida em **`UserCreationForm`**

Somente quando usuario estiver autenticado queremos que campo senha não apareça no formulario.

```python
class CustomUserCreationForm(forms.ModelForm):
	...

	def __init__(self, *args, **kwargs):
	  self.user = kwargs.pop('user', None)
	 ...
	  if self.user.is_authenticated:
	      del self.fields['password1']
	      del self.fields['password2']
	
	
	def save(self, commit=True):
	  # Save the provided password in hashed format
	  user = super().save(commit=False)
	  if self.user.is_authenticated:
	      user.set_password('123') # Senha padrão 123 para todos usuarios adicionados
	      user.force_change_password = True # força mudança de senha quando logar.
	  else:
	      user.set_password(self.cleaned_data["password1"])
	  if commit:
	      user.save()
	  return user
	
```

Lembrando que na views precisamos adicionar o parametro “user” para poder chamar no forms.

Adicione: `user=request.user` Assim no forms conseguimos pegar a instancia do usuario que está autenticado e adicionaremos as regras.

```python
# Adicionei aqui, todas as variaveis que tem Form.
def adicionar_usuario(request):
	user_form = CustomUserCreationForm(user=request.user)
	perfil_form = PerfilForm(user=request.user)

# Adicionei na view register tambem por que usamos a mesma class para formulário.
def register_view(request): 
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, user=request.user)
```

Agora vamos adicionar um campo no nosso modelo myUser. E adicionei essa função para pegar o valor da instancia desse campo. Rode o makemigrations e migrate para adicionar esse campo na tabela.

```python
# apps/contas/models.py
force_change_password = models.BooleanField(default=False)

def requires_password_change(self):
        return self.force_change_password
```

Vamos adicionar uma regra no login. Por que no login que vai verificar se é a primeira vez que usuario está entrando no sistema ou não. Então adicione esse codigo abaixo.

```python
def login_view(request):
	...
	if user is not None:
	  login(request, user)
	  
	  if user.is_authenticated and user.requires_password_change(): # Verifica
	      msg = 'Olá '+user.first_name+', como você pode perceber atualmente \
	              a sua senha é 123 cadastrado. Recomendamos fortemente \
	              que você altere sua senha para garantir a segurança da sua conta. \
	              É importante escolher uma senha forte e única que não seja fácil de adivinhar. \
	              Obrigado pela sua atenção!' 
	      messages.warning(request, msg)
	      return redirect('force_password_change') # Vai para rota de alterar senha.
	  else:
	      return redirect('home')
	
	else:
	  messages.error(request, 'Email ou senha inválidos')
	...
```

**Precisamos criar a rota que força a mudança de senha para usar o sistema.**

https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.update_session_auth_hash

apps/contas/views.py

```python
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Mudança de Senha Force (first_login)
@login_required
def force_password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_change_password = False # passa o parametro para False.
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'registration/password_force_change_form.html', context)

```

Lembra, no inicio quando criamos o formulário de mudança de senha e separamos o template formulário ? Então, para não ter que repetir o conteudo aqui nesse form vamos incluir o existente.

apps/contas/templates/registration/password_force_change_form.html

```python
{% extends 'base_dashboard.html' %}
{% block title %}Formulário Nova Senha{% endblock %}
{% block content_dash %} 
<div class="row p-5 bg-light">
    <h3>Entre com sua nova senha</h3>
    {% include "registration/change_form.html" %}
 </div>
{% endblock %}
```

apps/contas/urls.py

```python
path('nova-senha/', views.force_password_change_view, name='force_password_change'),
```

Agora é só testar.