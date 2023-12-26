# Comentários **(Replay)**

Dev: Letícia Lima

### **Criar Sub Comentário (replay)**

Poderiamos aproveitar a mesma views de criar um comentario de fizemos. Mas pra não ficar muito complicado de entender, achei melhor separar. Então vamos criar uma função. Vou chamar de `**responder_comentario**` .

apps/forum/views.py

```python
def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        message = 'Comentário Respondido com sucesso!'
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.usuario = request.user
            novo_comentario.parent_id = comentario_id
            novo_comentario.postagem = comentario.postagem
            novo_comentario.save()
            messages.info(request, message)
            return redirect('detalhe-postagem-forum',
                            slug=comentario.postagem.slug)
    return JsonResponse({'status': message})
```

apps/forum/urls.py

```python
path('responder-comentario/<int:comentario_id>/', 
			views.responder_comentario, name='responder-comentario'),
```

No template de detalhe da postagem atualizamos o botão de editar para fazer o collapse e mostrar o formullário de edição.

apps/forum/templates/comentarios/lista-comentario.html

```python
<a href="#" class="link-secondary"  
		data-bs-toggle="collapse" 
		data-bs-target="#responderComentario{{comentario.id}}" 
	  aria-expanded="false" 
		aria-controls="collapseResponderComentario">
		<i class="fa fa-reply fa-1x mx-1"></i>Responder</a>
```

Vamos criar um template para editar comentário e adicionar esse modelo abaixo. É bem parecido com o de edição o que muda são os atributos, que a chamada tem que ser diferente para não ta conflito.

apps/forum/templates/comentarios/editar-comentario.html

```python
<!-- Responder Comentario  -->
<div class="collapse mt-2" id="responderComentario{{comentario.id}}"> 
    <form method="POST" action="{% url 'responder-comentario' comentario.id %}"> 
        {% csrf_token %}
        {{ form_comentario.as_p }}
        <div class="d-flex justify-content-between">  
            <button type="submit" class="btn">
							<i class="fas fa-save fa-1x"></i> Salvar
						</button>    
            <button class="btn btn-white-sm" type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#responderComentario{{comentario.id}}" 
                aria-expanded="false" 
                aria-controls="collapseResponderComentario">
                <i class="fas fa-times fa-1x"></i>
            </button>  
        </div>  
    </form> 
</div>
```

Depois no template do detalhes da postagens no for de comentarios adicionar.

**`{% include "comentarios/responder-comentario.html" %}`**

### **Listar Sub Comentários (replay)**

Agora precisamos ajustar e tratar na lista para mostrar os comentarios respondidos referente ao comentario “pai”. Vamos listar os comentários “filho”. 

Lembra da propriedade que colocamos no modelo de comentários.

```python
@property
def children(self):
	 return PostagemForumComentario.objects.filter(
							parent=self).order_by('-data_criacao').all()
```

Vai fazer sentido aqui agora. Vamos fazer um loop para pegar todos os comentários “filho” do comentário “pai”. Por isso vamos fazer o for e tratar isso no template. 

Estou aproveitando o mesmo template que usamos na lista de comentário e subistitui parametros.

**`{% for child_comentario in comentario.children %}`**

apps/forum/templates/comentarios/lista-responder-comentario.html

```html
<!-- Sub Comentarios, os "parentes" -->
<div class="ms-5">
    {% for child_comentario in comentario.children %} 
    <div class="d-flex mt-4"> 
        <div class="bg-light border rounded-3 w-100 p-3">
            <div class="d-flex justify-content-between">  
                <div>
                    <img src="{{child_comentario.usuario.perfil.foto.url}}" class="rounded-circle mr-2" width="30" height="30"> 
                    <strong class="fst-italic">{{child_comentario.usuario.first_name}} {{child_comentario.usuario.last_name}}</strong>
                </div>  
                <span class="mx-3 fst-italic">{{child_comentario.data_criacao}}</span> 
            </div> 
            <p class="text-break mx-3 mt-3">{{child_comentario.comentario}}</p> 
            <div class="d-flex justify-content-start">  
                {% if request.user == child_comentario.usuario %}
                <a href="#" class="link-success" 
										data-bs-toggle="collapse" 
										data-bs-target="#editarSubComentario{{child_comentario.id}}" 
                    aria-expanded="false" 
										aria-controls="collapseEditarSubComentario"><i class="fas fa-edit mx-2"></i></a>
                <a href="#" class="link-danger"><i class="fas fa-trash fa-1x mx-1"></i></a> 
                {% endif %}
            </div>  
        </div>  
    </div>  
    {% endfor %} 
</div>
```

No detalhes da postagem precisamos adicionar  **`{% if comentario.is_parent %}`** para mostrar os comentarios “filho” relacionados com comentario “pai”. E o template da lista que acabamos de criar.

apps/forum/templates/detalhe-postagem-forum.html

```html
{% for comentario  in postagem.postagem_comentario.all %}
{% if comentario.is_parent %}
{% include "comentarios/lista-comentario.html" %}
{% include "comentarios/editar-comentario.html" %}
{% include "comentarios/responder-comentario.html" %}
{% include "comentarios/lista-responder-comentario.html" %}
{% endif %}
{% endfor %}
```

### **Editar Sub Comentário (replay)**

Agora fica mais simples, pois podemos aproveitar a views de **`editar-comentario`** e enviar o form para atualizar os dados. 

```python
<!-- Editar subComentario  -->
<div class="collapse mt-2" id="editarSubComentario{{child_comentario.id}}"> 
  <form method="POST" action="{% url 'editar-comentario' child_comentario.id %}"> 
      {% csrf_token %}
      <textarea class="form-control" rows="3" name="comentario" id="comentario" 
          placeholder="Escreva um comentário...">{{child_comentario.comentario}}</textarea>  
      <div class="d-flex justify-content-between">  
          <button type="submit" class="btn">
						<i class="fas fa-save fa-1x"></i> Salvar
					</button>    
          <button class="btn btn-white-sm" type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#editarSubComentario{{child_comentario.id}}" 
              aria-expanded="false" 
              aria-controls="collapseEditarSubComentario">
              <i class="fas fa-times fa-1x"></i>
          </button>  
      </div>  
  </form> 
</div>
```

No tempalte de lista-responder-comentario que criamos para os comentarios “filho” vamos atualizar o template assim.

apps/forum/templates/comentarios/lista-responder-comentario.html

```html
<!-- Sub Comentarios, os "parentes" -->
<div class="ms-5">
    {% for child_comentario in comentario.children %} 
    <div class="d-flex mt-4"> 
        <div class="bg-light border rounded-3 w-100 p-3">
            <div class="d-flex justify-content-between">  
                <div>
                    <img src="{{child_comentario.usuario.perfil.foto.url}}" class="rounded-circle mr-2" width="30" height="30"> 
                    <strong class="fst-italic">{{child_comentario.usuario.first_name}} {{child_comentario.usuario.last_name}}</strong>
                </div>  
                <span class="mx-3 fst-italic">{{child_comentario.data_criacao}}</span> 
            </div> 
            <p class="text-break mx-3 mt-3">{{child_comentario.comentario}}</p> 
            <div class="d-flex justify-content-start">  
                {% if request.user == child_comentario.usuario %}
                <a href="#" class="link-success" 
										data-bs-toggle="collapse" 
										data-bs-target="#editarSubComentario{{child_comentario.id}}" 
                    aria-expanded="false" 
										aria-controls="collapseEditarSubComentario">
										<i class="fas fa-edit mx-2"></i></a>
                <a href="#" class="link-danger"><i class="fas fa-trash fa-1x mx-1"></i></a> 
                {% endif %}
            </div>  
        </div>  
    </div> 

     <!-- Editar subComentario  -->
     <div class="collapse mt-2" id="editarSubComentario{{child_comentario.id}}"> 
        <form method="POST" action="{% url 'editar-comentario' child_comentario.id %}"> 
            {% csrf_token %}
            <textarea class="form-control" rows="3" name="comentario" id="comentario" 
                placeholder="Escreva um comentário...">{{child_comentario.comentario}}</textarea>  
            <div class="d-flex justify-content-between">  
                <button type="submit" class="btn">
									<i class="fas fa-save fa-1x"></i> Salvar
								</button>    
                <button class="btn btn-white-sm" type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#editarSubComentario{{child_comentario.id}}" 
                    aria-expanded="false" 
                    aria-controls="collapseEditarSubComentario">
                    <i class="fas fa-times fa-1x"></i>
                </button>  
            </div>  
        </form> 
    </div>

    {% endfor %} 
</div>
```

Adicionar o botão

```html
<a href="#" class="link-success" 
	data-bs-toggle="collapse" 
	data-bs-target="#editarSubComentario{{child_comentario.id}}" 
	aria-expanded="false" 
	aria-controls="collapseEditarSubComentario"><i class="fas fa-edit mx-2"></i></a>
```

  

### **Deletar Sub Comentário  (replay)**

Novamente, aproveitando a função deletar-comentario e vamos passar o identificador do comentario “filho” para remover.

apps/forum/templates/comentarios/lista-responder-comentario.html
```html
<form method="POST" action="{% url 'deletar-comentario' child_comentario.id %}">
    {% csrf_token %}  
    <button type="submit" class="link-danger btn btn-transparent m-0 p-0">
			<i class="fas fa-trash fa-1x mx-1"></i>
		</button> 
</form>
```