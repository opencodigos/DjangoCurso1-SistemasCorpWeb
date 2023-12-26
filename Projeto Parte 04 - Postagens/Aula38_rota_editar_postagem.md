# **Rota Editar Postagem**

**Dev: Letícia Lima**

Vamos criar um view para editar uma postagem. Lembrando que somente usuarios autenticados podem editar postagem. Por isso o decorador `**@login_required.**` Mesmo template que usamos para criar uma postagem, podemos usar para editar uma postagem. Até o `**PostagemForumForm**` é o mesmo. 

<aside>
⚠️ **Vamos supor que você precisa tratar os campos de maneira diferente da rota de edição e criação. Ai nesse caso eu concordo em criar uma outra classe no forms. 
Exemplo: `EditPostagemForumForm`  e trata os campos como precisar para rota de edição. Geralmente eu uso para desativar um campo deixar ele desabilitado.
Nesse caso nosso não vai mudar nada. Todos os campos que tem no forms eu vou usar para editar.**

</aside>

Para editar uma postagem o usuario precisa está autenticado. Por isso o decorator ***@login_required.***

apps/forum/views.py

```python
from django.contrib.auth.decorators import login_required

@login_required
def editar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
						messages.warning(request, 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!')
            return redirect('editar-postagem-forum', id=postagem.id)
    else:
        form = PostagemForumForm(instance=postagem)
    return render(request, 'form-postagem-forum.html', {'form': form})
```

apps/forum/urls.py

```python
path('editar-postagem-forum/<int:id>/', views.editar_postagem_forum, name='editar-postagem-forum'),
```

Como estamos aproveitando o mesmo formulário que usamos para criar uma postagem. Vamos adicionar uma regra. ***(Por enquanto, depois vamos fazer algo diferente)***

apps/forum/templates/form-postagem-forum.html

```python
<h4>{% if request.path == '/forum/criar-postagem-forum/' %} Criar Postagem {% else %} Editar Postagem {% endif %} </h4>
```

No formulário de detalhes a gente adiciona o botão para ir para rota de editar uma postagem.

apps/forum/templates/detalhe-postagem-forum.html

```python
<a class="btn btn-warning" href="{% url 'detalhe-postagem-forum' %}"><i class="fas fa-edit"></i></a>
```

Só que tem um problema, do jeito que está mostrando a tag qualquer usuario vai tentar editar a postagem. 

E isso nao pode acontecer. 

**Por isso vamos adicionar uma regra para que somente o autor da postagem possa editar.**

```python
{% if postagem.usuario == request.user %}
<a class="btn btn-warning" 
				href="{% url 'editar-postagem-forum' postagem.id %}">
		<i class="fas fa-edit"></i></a>  
<a class="btn btn-danger" href="#"><i class="fas fa-trash"></i></a>  
{% endif %}
```

Mesmo assim se acessarmos a rota assim:

[http://localhost:8000/forum/editar-postagem-forum/](http://localhost:8000/forum/editar-postagem-forum/5/){ID} de uma postagem que não é nossa. Ela vai acessar. 

Então vamos reforçar isso na view. Colocando se o usuario for **administrador** ai ele pode editar qualquer coisa. Senão é somente se for **autor da postagem.**

```python
# Verifica se o usuário autenticado é o autor da postagem
if request.user != postagem.usuario and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
	 return redirect('postagem-forum-list')  # Redireciona para uma página de erro ou outra página adequada
```

**Atualizamos a view assim:**

```python
from django.contrib.auth.decorators import login_required

@login_required
def editar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    
    # Verifica se o usuário autenticado é o autor da postagem
    if request.user != postagem.usuario and not (
            ['administrador', 'colaborador'] in request.user.groups.all() 
						or request.user.is_superuser):
# Redireciona para uma página de erro ou outra página adequada
            return redirect('postagem-forum-list')  
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Seu Post '+ postagem.titulo +' \
                foi atualizado com sucesso!')
            return redirect('editar-postagem-forum', id=postagem.id)
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = PostagemForumForm(instance=postagem)
    return render(request, 'form-postagem-forum.html', {'form': form})
```

Com base nisso já conseguimos testar e ter um resultado legal.