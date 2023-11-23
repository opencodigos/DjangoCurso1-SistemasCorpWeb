# **Permissões de Acesso**

Dev: Letícia Lima

Agora vamos aplicar permissões de acesso nessa rota, por exemplo. Usuario que está no grupo administrador pode editar qualquer usuario e acessar as informações. Colaborador pode visualizar os dados de qualquer usuário mas não pode deletar, Usuario pode ver somente as informações do proprio.

Criamos 2 rotas para atualizar o usuário. Essas duas rotas a gente separou para instancia autenticada e outra recebe um id para estar atualizando os dados.

**Vamos aplicar permissões de acesso utilizando decorrator:** https://docs.djangoproject.com/en/4.2/topics/http/decorators/ 

https://docs.djangoproject.com/en/4.2/topics/class-based-views/intro/#id1

Cria uma regra, nesse caso adicionei que somente quem está no grupo administrador e colaborador pode acessar essa rota.

apps/contas/permissions.py

```python
from django.shortcuts import redirect
from django.contrib import messages

def grupo_colaborador_required(groups):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('home')
                # return HttpResponseForbidden('Você não tem permissão para acessar esta página.')
        return wrapper
    return decorator
```

Depois na view. Chamamos esse decorator assim.

Defino que somente usuário que pertence ao grupo administrador e colaborador podem editar outros usuarios.

```python
@login_required()
@grupo_colaborador_required(['administrador','colaborador'])
def atualizar_usuario(request, user_id):
	...
```

Como tratar campos para diferentes tipos de grupos.

Por exemplo, para usuarios administradores e colaboradores o campo `**is_activate**` pode aparecer. Agora para grupo usuario nao pode.

apps/contas/forms.y

```python
def __init__(self, *args, **kwargs):
	self.user = kwargs.pop('user', None) # get the 'user' from kwargs dictionary
	super(UserChangeForm, self).__init__(*args, **kwargs)
  ...
  if not self.user.groups.filter(name__in=['administrador','colaborador']).exists():
      for group in ['is_active']: 
          del self.fields[group]
```

```python
# self.user = kwargs.pop('user', None)
# pega a instancia do usuario autenticado

...
form = UserChangeForm(request.POST, instance=user, user=request.user)
```

Feito isso o campo is_activate esta com a regra de aparecer somente para administrador e colaborador. 

Com base nisso, é possivel criar variações de permissão e customizar o formulário tambem.