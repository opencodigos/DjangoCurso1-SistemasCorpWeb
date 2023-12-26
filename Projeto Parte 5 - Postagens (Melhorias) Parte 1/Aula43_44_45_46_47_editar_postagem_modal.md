# **Editar Postagem (Modal)**

**Dev: Letícia Lima**

### Views (Função)

**Primeiro quais as rotas que temos o `botão de editar uma postagem` ?** 

- **Pagina Forum (Homepage)**
- **Pagina** **DashBoard (Lista de Postagens)**
- **Perfil (Lista de Postagem do usuario)**

**São 3 rotas diferentes que tem o mesmo botão e formulário para editar uma postagem.**

Podemos usar um modal para editar. Ficaria interessante. O *bom nessa aula vamos sair um pouco da bolha.*

**`OBS: Não vamos usar JS e CSS.`**

Essa função **editar_postagem_forum** de editar uma postagem, será enviado o form para o metodo post para tratar o formulário e salvar. 

Como é um **modal** não vai ter um template para renderizar essa view. Não precisamos desse `**return render()` mas precisamos tratar esse `redirect()` .** 

Por que nas rotas **Pagina Forum (Homepage), Pagina** **DashBoard (Lista de Postagens), Perfil (Lista de Postagem do usuario).** Após editar será redirecionado para uma rota “anterior” ou “atual” que estamos. E o redirecionamento de cada uma é diferente. E como vamos usar a mesma função vamos precisar tratar isso. 

**Uma solução que encontrei é fazer a requisitão do path que estou. Assim independente da rota não vamos ter problemas de redirecionamento.**

Inicialmente vamos fazer assim. Toda vez que salvar um formulário manda pra essa view e salva. Depois redireciona para ‘**detalhes-postagem-forum**’. 

apps/forum/views.py 

```python
from django.http import JsonResponse

@login_required
def editar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.user != postagem.usuario and not (
        ['administrador', 'colaborador'] in request.user.groups.all() 
				or request.user.is_superuser):
        return redirect('lista-postagem-forum') # Adicionar uma rota "sem permissão"
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
						messages.warning(request, 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!')
            return redirect('detalhe-postagem-forum', id=postagem.id)
		return JsonResponse({'status': 'Ok'}) # Coloca por enquanto.
```

Fazendo isso como o formulário vai ser renderizado ? 

### Rota Detalhes da Postagem

Rota “**Detalhes**” vamos adicionar uma instancia. **`form = PostagemForumForm(instance=postagem)` toda vez que abrirmos o modal para editar ele vai carregar os dados o objeto.**

```python
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=postagem)
    context = {'form': form, 'postagem': postagem}
    return render(request,'detalhe-postagem-forum.html', context)
```

Modal com form **`action="{% url 'editar-postagem-forum' postagem.id %}"` Pega os dados do formulário do modal e manda pra essa view e salva.**

Não podemos esquecer de colocar o Identificador no modal para chamar no botão depois. `**id="editarPostagemModal{{postagem.id}}**` **mesmo metodo que utilizamos no delete.**

apps/forum/template/model-form-postagem-forum.html

```python
<div class="modal modal-lg fade" id="editarPostagemModal{{postagem.id}}" tabindex="-1" 
	aria-labelledby="editarPostagemModalLabel" aria-hidden="true"> 
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h4>Editar Postagem</h4>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
        <form method="post" action="{% url 'editar-postagem-forum' postagem.id %}" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary mx-2">Criar</button>
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
        </form>
			</div>
		</div>
	</div>
</div>
```

**Vamos testar na rota de Detalhes da postagem.**

apps/forum/templates/detalhe-postagem-forum.html

```python
...
<div class="col-md-8"> 
{% include 'components/messages.html' %}
...
<div class="div"> 
    {% if postagem.usuario == request.user %}
    <a class="btn btn-warning" data-bs-toggle="modal" href="#editarPostagemModal{{postagem.id}}" role="button"> # Adiciona
        <i class="fas fa-edit"></i></a> 
    <a class="btn btn-danger" data-bs-toggle="modal" href="#confirmarExclusaoModal{{postagem.id}}" role="button">
        <i class="fas fa-trash"></i></a>  
    {% endif %}
</div> 
  ...
</div>
{% include "modal-form-postagem-forum.html" %} # Adiciona 
{% include "modal-deletar-postagem-forum.html" %}
{% endblock %}
```

 

Se testarmos agora vai ta funcionando legal. Eu achei interessante trazer isso pra voces sem usar JS.
Que não mudaria muita coisa inicialmente. (depois vemos isso)

### Rota Perfil do Usuário

Temos uma lista de postagens. É um pouco diferente do detalhe da postagem onde já estamos dentro do objeto e temos as informações unica de ‘facil acesso’. 

No template **perfil.html** temos um ***for*** assim para mostrar as postagens relacionadas com perfil do usuário. Só que agora como vamos ter um **modal para editar** os dados da postagem de cada objeto. 
**Então teremos que ter todas as instancias desses formulários de cada objeto.** 

Na view vamos tratar esses dados, criar esse for. Pegar todas os form e adicionar num dicionario. 
Chamei de **`form_dict`**.

```python
form_dict = {}
for el in perfil.user_postagem_forum.all():
    form = PostagemForumForm(instance=el) 
    form_dict[el] = form
```

Adiciona no **context** para renderizar no template.

```python
def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)

    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form

    return render(request, 'perfil.html', {'obj': perfil,'form_dict':form_dict})
```

Atualizamos o template perfil assim:

apps/perfil/template/perfil.html

```python
{% for postagem, form in form_dict.items %} # agora é dicionario então coloca .items e form para cada objeto que aparecer no loop.
<div class="p-3 mb-3 rounded-3 shadow-sm">
    <div class="align-items-center">
        <div class="d-flex justify-content-between">
            <h5><a href="{% url 'detalhe-postagem-forum' postagem.id %}">{{postagem.titulo}}</a></h5>
            <div class="div">
                {% if postagem.usuario == request.user %}
                <a class="btn btn-warning" data-bs-toggle="modal" href="#editarPostagemModal{{postagem.id}}" role="button"> # Adiciona Botão
                    <i class="fas fa-edit"></i></a>  
                <a class="btn btn-danger" data-bs-toggle="modal" href="#confirmarExclusaoModal{{postagem.id}}" role="button">
                    <i class="fas fa-trash"></i></a>  
                {% endif %}
            </div>
        </div>  
        <div class="text-truncate-box"> 
            <p class="text-truncate">{{postagem.descricao|safe|truncatechars:230}}</p> 
        </div>
    </div>
    <div class="d-flex justify-content-between align-items-center">
        <div class="align-items-center">
            <small class="text-muted">{{postagem.data_publicacao}}</small>
        </div>
    </div>
</div> 
{% include "modal-form-postagem-forum.html" %} # Adiciona formulario do modal
{% include "modal-deletar-postagem-forum.html" %}
{% endfor %}
```

Feito isso pessoal não precisa tratar mais nada. Por que estamos usando o mesmo modal, mesma views para fazer o post do formulário. **Agora é testar !!!**

### Rota Lista de Postagens (Dashboard)

Nessa lista de postagens do dashboard não é muito diferente do que fizemos na rota de perfil. A diferença é que estamos usando a mesma view para listar as postagens que tem na rota /forum da homepage, certo ? **Isso não é um problema.** Vamos conseguir fazer tudo que precisamos. Então adicionamos nosso contexto do formulário para mostrar nessa view tambem. 

```python
def lista_postagem_forum(request):
    form_dict = {}
    ...
    # Como existe uma lista de objetos, para aparecer o formulário 
		# correspondente no modal precisamos ter um for
    for el in postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
context = {'postagens': postagens,'form_dict': form_dict}
return render(request, template_view, context)
```

apps/forum/templates/dashboard/dash-lista-postagem-forum.html

```python
{% for postagem, form in form_dict.items %} # Adiciona
  <tbody>
      <tr>
          <td scope="row">{{ postagem.id }}</td>
          <td scope="row">{{ postagem.usuario.first_name }} {{ postagem.usuario.last_name }}</td>
          <td scope="row">{{ postagem.titulo }}</td>
          <td scope="row">{{ postagem.data_criacao|date:'d/m/Y'}}</td>
          <td scope="row">{{ postagem.data_publicacao|date:'d/m/Y'}}</td>
          <td scope="row">
              {% if postagem.ativo %}
              <span class="badge bg-success rounded-pill d-inline">Ativado</span> 
              {% else %}
              <span class="badge bg-danger rounded-pill d-inline">Desativado</span>  
              {% endif %}
          </td>
          <td scope="row">
              <a class="link-warning" href="{% url 'detalhe-postagem-forum' postagem.id %}">
                  <i class="fas fa-eye mx-2"></i></a>
              <a class="ml-2 link-secondary" data-bs-toggle="modal" href="#editarPostagemModal{{postagem.id}}" role="button"> # adiciona botão para abrir o modal
                  <i class="far fa-file mx-2"></i></a>
              <a class="ml-3 link-danger" data-bs-toggle="modal" href="#confirmarExclusaoModal{{postagem.id}}" role="button">
                  <i class="fas fa-trash mx-2"></i></a>
              {% include "modal-form-postagem-forum.html" %} # Adiciona
              {% include "modal-deletar-postagem-forum.html" %}
          </td>
      </tr>
  </tbody> 
  {% empty %}
  <p>Nenhuma poste cadastrado.</p>
  {% endfor %}
```

Feito isso podemos testar e ver o resultado. Tem alguns ajuste para fazer ainda, por exemplo o redirecionamento como havia explicado para voces no inicio. 

**Outro detalhe que gostaria de compartilhar com vocês** é a questão dos nomes das variaveis. Perceberam que estou mantando o mesmo nome em todos os templates ? Isso é uma boa pratica pra não confundir e manter um codigo **clean**. 

### Tratar o Redirecionamento

**Uma solução que encontrei é fazer a requisitão do path que estou. Assim independente da rota não vamos ter problemas de redirecionamento.**

No formulário faça essa mudança. Adiciona um input tipo hidden com valor da **`{{ request.path }}`**. Assim conseguimos saber que pagina estamos.

apps/forum/templates/modal-form-postagem-forum.html

```python
<form method="post" action="{% url 'editar-postagem-forum' postagem.id %}" enctype="multipart/form-data">
	{% csrf_token %}
	{{ form.as_p }}
	<input type="hidden" name="redirect_route" value="{{ request.path }}"> # Adiciona esse input tipo hidden com valor {{ request.path }}
	<button type="submit" class="btn btn-primary mx-2">Criar</button>
	<button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
</form>
```

Na views vamos fazer essa mudança

apps/forum/views.py

```python
@login_required 
def editar_postagem_forum(request,id):
    redirect_route = request.POST.get('redirect_route', '') # Adiciona
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!' # atualizei a mensagem
    if request.user != postagem.usuario and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
        return redirect('lista-postagem-forum') # Adicionar uma rota "sem permissão"
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            messages.warning(request, message)
            return redirect(redirect_route) # Faz o redirect de acordo com a rota que estou.
    return JsonResponse({'status': message}) # isso deixa assim por enquando. Vai que futuramente utilizaremos algo a mais.
```

**Bom pessoal é isso. Vocês devem perceber o resultado.**

### Por exemplo:

Estou na rota `**dashboard/lista-postagem/**` quando abre o modal para editar um objeto da lista e clica em salvar, deve redirecionar para `**dashboard/lista-postagem/**`

Estou na rota `**detalhe-postagem-forum/{ID}/**` independente do objeto, quando abre o modal e clica em salvar, deve redirecionar para `**detalhe-postagem-forum/{ID}/**` 

Estou na rota `**perfil/slug:username/**` no meu perfil, quando abre o modal e clica em salvar, deve redirecionar para `**perfil/slug:username/**`

**Faz esses testes e verificar se isso aconteceu. Ok.**

### DELETE

O delete é mesmo metodo mas muda um detalhe. Por exemplo quando estamos na rota de detalhe `**detalhe-postagem-forum/{ID}/**` **se apagar esse objeto não tem como voltar para esse objeto**. Por que o mesmo não existe mais, certo ?

apps/forum/template/modal-delete-postagem-forum.html

```python
<form method="post" action="{% url 'deletar-postagem-forum' postagem.id %}">
    {% csrf_token %}
		<input type="hidden" name="redirect_route" value="{{ request.path }}"> # Adiciona 
    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
    <button type="submit" class="btn btn-danger">Excluir</button>
</form>
```

apps/forum/views.py

```python
import re

@login_required 
def deletar_postagem_forum(request, id): 
    redirect_route = request.POST.get('redirect_route', '') # adiciono saber a rota que estamos
    print(redirect_route)
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+postagem.titulo+' foi deletado com sucesso!' # atualizei a mesnagem aqui
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)
        
				if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('lista-postagem-forum')
        return redirect(redirect_route)

    return JsonResponse({'status':message})
```

No exemplo acima, primeiro verificamos se **`redirect_route`** é exatamente igual a **`/forum/detalhe-postagem-forum/`**. Se for o caso, retornamos o redirecionamento para **`lista-postagem-forum`** .

Em seguida, se a URL não corresponder ao caso acima, continuamos com a expressão regular para capturar o valor correspondente de **`redirect_route` .**

*Bem legal neh.*

*Chega de modal rsrs Depois podemos explorar mais, com Javascript talvez. Isso é pra vocês ter uma ideia do poder do python e django. **Que ate mesmo sem JS podemos fazer coisas legais.***