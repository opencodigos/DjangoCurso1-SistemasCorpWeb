# **Rota Deletar Postagem**

Dev: Letícia Lima

Vamos criar uma view para deletar uma postagem. 
Essa view precisa receber o **ID do objeto** para deletar e inicialmente colocamos um *redirect* para lista de postagens da rota *forum/*. Bem simples de inicio.

apps/forum/views.py

```python
@login_required 
def deletar_postagem_forum(request, id): 
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, 'Seu Post '+ postagem.titulo +' foi deletado com sucesso!')
        return redirect('lista-postagem-forum')
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem})
```

apps/forum/urls.py

```python
path('deletar-postagem-forum/<int:id>/', views.deletar_postagem_forum, name='deletar-postagem-forum'),
```

Já conseguimos testar. Se pegar o ID de algum objeto. **[localhost:8000/forum/deletar-postagem-forum/{ID}/](http://localhost:8000/forum/deletar-postagem-forum/{ID}/)** Do jeito que está objeto é deletado sem nenhum aviso. Assim fica muito ruim, vamos adicionar um botão para abrir um modal perguntando se deseja mesmo deletar o objeto.

Vamos tratar isso no template. Para ficar mais intuitivo pensei em fazermos um modal.

**Simples com bootstrap sem usar JS e CSS.**

Na rota de **detalhes da postagem** vamos atualizar esse botão e colocar uma chamada para o modal.

apps/forum/templates/detalhe-postagem-forum.html

```python
<a class="btn btn-danger" data-bs-toggle="modal" 
		href="#confirmarExclusaoModal{{postagem.id}}" role="button">
		<i class="fas fa-trash"></i></a>
```

Vamos criar um template o modal.

Por que colocamos assim: `**confirmarExclusaoModal{{postagem.id}}**` esse **`{{postagem.id}}`** para ter certeza que vai pegar o objeto certo para deletar. **Isso vai ser muito util quando tivermos um `for` com varios registro com botão de deletar.**

apps/forum/templates/modal-deletar-postagem-forum.html

```html
<div class="modal fade" id="confirmarExclusaoModal{{postagem.id}}" tabindex="-1" aria-labelledby="confirmarExclusaoModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="confirmarExclusaoModalLabel">Atenção Usuario ! <i
						class="link-danger fas fa-exclamation-triangle me-2"></i></h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				 <p>Você tem certeza de que deseja excluir a postagem "{{ postagem.titulo }}"?</p> 
			</div>
			<div class="modal-footer">
	        <form method="post" action="{% url 'deletar-postagem-forum' postagem.id %}">
	            {% csrf_token %}
	            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
	            <button type="submit" class="btn btn-danger">Excluir</button>
	        </form>
	    </div>
		</div>
	</div>
</div>
```

Depois pessoal muito importante. Precisamos incluir esse template que criamos do modal na rota de detalhes, **aonde está nosso botão.**

E depois incluimos. Assim podemos aproveitar esse mesmo modal em outras views se tiver. *(vai ter rsrsrs)*

**Obs: modal-deletar-postagem-forum.html Não tem view. ele é um modal. Dentro dele tem um form que envia a resposta para view.**

```python
{% include "modal-deletar-postagem-forum.html" %}
```

**Adiciona assim:**
```python
{% extends "base.html" %}
{% block title %}Detalhes da Postagem{% endblock %}
{% block content %}
<div class="container mt-3">
    <div class="row">
        <div class="col-md-8"> 
            <div class="bg-light p-3">  
                <div class="d-flex justify-content-between">
                    <span>{{postagem.data_publicacao}}</span> <br> 
                    <div class="div"> 
                        {% if postagem.usuario == request.user %}
												<a class="btn btn-warning" href="{% url 'editar-postagem-forum' postagem.id %}"><i class="fas fa-edit"></i></a>  
												<a class="btn btn-danger" data-bs-toggle="modal" href="#confirmarExclusaoModal{{postagem.id}}" role="button"><i class="fas fa-trash"></i></a>
												{% endif %}
                    </div> 
                </div> 
                <span>Autor: {{postagem.usuario.first_name}}</span>
                <div class="mt-3">  
                    <h2>{{postagem.titulo}}</h2>
                    <p>{{postagem.descricao}}</p>
                    {% if postagem.anexar_imagem %}
                    <a href="{{postagem.anexar_imagem.url}}" target="_blank">Anexo</a>   
                    {% endif %}
                </div> 
            </div> 
        </div>
    </div>
</div>
{% include "modal-deletar-postagem-forum.html" %}
{% endblock %}
```