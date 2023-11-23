# **Multiplos Anexos na Postagem (Bonus)** (Editar Postagem)

Dev: Letícia Lima

### Rota Editar Postagem

Na parte de editar as postagens vamos modificar essa função **`editar_postagem_forum`** é a função principal para tratar e salvar as postagens, indenpendente da rota que estamos.

O primeiro passo é deixar a view bem parecida com o que ficamos na rota cadastro. Vai mudar algumas coisas, como por exemplo quando editamos um objeto temos que contar e saber a quantidade anexo a postagem já tem e quantos ainda podem ser enviados. 

Isso podemos pegar o objeto a postagem e acessar todos os arquivos relacionados com essa postagem. 

`**contar_imagens = postagem.postagem_imagens.count()` Conta quantos anexos tem.**

**`postagem_imagens = request.FILES.getlist('postagem_imagens')` Quantos o usuario está enviando.**

Nisso aplicamos uma condição. `**if contar_imagens + len(postagem_imagens) > 5:`** 

apps/forum/views.py

```python
# Editar Postagem (ID)
@login_required
def editar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '') 
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!'
    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != postagem.usuario and not (
        any(grupo.name in lista_grupos for grupo in request.user.groups.all()) or request.user.is_superuser):
        messages.warning(request, 'Seu usuário não tem permissões para acessar essa pagina.')
        return redirect('lista-postagem-forum')  # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            
            contar_imagens = postagem.postagem_imagens.count() # Quantidade de imagens sque já tenho no post
            postagem_imagens = request.FILES.getlist('postagem_imagens') # Quantidade de imagens que estou enviando para salvar

            if contar_imagens + len(postagem_imagens) > 5:
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in postagem_imagens: # for para pegar as imagens e salvar.
                    models.PostagemForumImagem.objects.create(postagem=form, imagem=f)
                    
                messages.warning(request,message)
                return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form) 
    return JsonResponse({'status': message}) # Coloca por enquanto.
```

**Mudamos no modal do form.**

apps/forum/template/modal-form-postagem-forum.html

```python
...
<div class="modal-body">
	  <form method="post" action="{% url 'editar-postagem-forum' postagem.id %}" enctype="multipart/form-data">
	      {% csrf_token %}
	      {{ form.as_p }} 
				<input type="hidden" name="redirect_route" value="{{ request.path }}">
	      <button type="submit" class="btn btn-primary mx-2">Salvar</button>
	      <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
	  </form>

		<div class="d-flex g-3"> # Adicionamos esse for para exibir as imagens no formulário
			{% for img in postagem.postagem_imagens.all %} # Pegando todas as imagens relacionadas com a postagem
			<div class="position-relative p-2">
					<a href="#" class="position-absolute badge bg-danger">
							<i class="fas fa-times"></i>
					</a>
					<img src="{{ img.imagem.url }}" class="img-fluid rounded" alt="{{img.id}}" width="100"> 
			</div>
			{% endfor %}
		</div>
</div>
...
```

Feito isso conseguimos testar.  só não conseguimos remover a imagem, mas validar se está salvando e verificando 5 anexos. Já está funcionando.