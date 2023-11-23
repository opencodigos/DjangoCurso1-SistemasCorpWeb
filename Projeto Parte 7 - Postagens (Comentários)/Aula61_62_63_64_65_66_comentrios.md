# Comentários

Dev: Letícia Lima

### **Criar modelo de Comentários**

Vamos criar um modelo para registrar os comentarios de cada usuario relacionado com a postagem.

apps/forum/views.py

```python
class PostagemForumComentario(models.Model):
    usuario = models.ForeignKey(user, on_delete=models.CASCADE, 
																	related_name='usuario_comentario')
    postagem = models.ForeignKey(PostagemForum, 
														on_delete=models.CASCADE, related_name="postagem_comentario") 
    parent = models.ForeignKey('self', 
											on_delete=models.CASCADE, blank=True, null=True, related_name='+') 
    data_criacao = models.DateTimeField(auto_now_add=True)
		comentario = models.TextField(blank=True, null=True)     
   
    @property
    def children(self):
        return PostagemForumComentario.objects.filter(parent=self).order_by('-data_criacao').all()

    @property
    def is_parent(self): 
        if self.parent is None:
            return True
        return False 
    
    def __str__(self):
        return '{} - {}'.format(self.usuario.email, self.postagem.titulo)

		class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data_criacao']
```

**Documentação sobre  @property** https://docs.python.org/3/library/functions.html#property

A propriedade **`children`** retorna os comentários filhos associados a um comentário específico, enquanto a propriedade **`is_parent`** verifica se um comentário é um comentário pai ou não, com base na existência de um valor nulo para o campo **`parent`**.

**Documentação:** https://docs.djangoproject.com/pt-br/4.2/ref/models/fields/#django.db.models.ForeignKey

Quando define **`related_name='+'`** em um relacionamento ForeignKey, isso indica que você não deseja criar um relacionamento inverso. O sinal de "+" é usado para especificar que nenhum nome de relacionamento inverso que será criado. Ao usar **`related_name='+'`**, você está informando ao Django que não deseja criar um relacionamento inverso. Isso pode ser útil em situações em que você não precisa ou não deseja acessar o objeto relacionado por meio de modelo.

```bash
#Rodar
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

### **Criar Comentário**

Vamos criar uma class no forms. Terá somente um campo “comentario” e estou colocando atributos necessarios para tipo textarea.

apps/forum/forms.py

```python
class PostagemForumComentarioForm(forms.ModelForm):
    class Meta:
        model = PostagemForumComentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3})
        }
```

No detalhes da postagem adicionamos o contexto para renderizar no template nosso formulário. 
Estou chamando de **`form_comentario`** para diferenciar do formulário da postagem que é **`form`** 

apps/forum/views.py

```python
## Detalhes da postagem
def detalhe_postagem_forum(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    form = PostagemForumForm(instance=postagem)
    form_comentario = PostagemForumComentarioForm()
    context = {'form': form,
               'postagem': postagem,
               'form_comentario':form_comentario}
    return render(request,'detalhe-postagem-forum.html', context)
```

Vamos incorporar esse form_comentario no template de detalhes da postagem, uma vez que é nesse template que o formulário para registrar um comentário será exibido. Implementei uma regra que mostra o formulário de comentários se o usuário estiver autenticado, caso contrário, exibirá um botão para efetuar o login ou se cadastrar no sistema.

apps/forum/templates/detalhe-postagem-forum.html

```python
# criei comentarios/adicionar-comentario.html
# Depois aplica um include no template.

<div class="mt-5">  
  {% if user.is_authenticated %} 
  <form method="POST" action="#">
      {% csrf_token %}
      {{ form_comentario.as_p }}
      <button type="submit" class="btn btn-outline-primary">Enviar</button>
  </form> 
  {% else %} 
  <div class="text-center mb-3">
      <h4>Olá,</h4>
      <p>Você precisa fazer login no sistema para comentar.</p>
      <a class="btn btn-dark" href="{% url 'login' %}">
				<i class="fas fa-sign-in-alt fa-2x"></i>
			</a>
  </div>  
  {% endif %} 
</div>
```

Ainda não vai está funcionado por que precisamos criar a view para adicioanr um comentário. Vou chamar de **`adicionar_comentario`**. 

apps/forum/views.py

```python
def adicionar_comentario(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    message = 'Comentário Adcionado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.postagem = postagem
            comentario.save() 
            messages.warning(request, message)
            return redirect('detalhe-postagem-forum', slug=postagem.slug)
    return JsonResponse({'status': message})
```

apps/forum/urls.py

```python
path('adicionar-comentario/<str:slug>/', 
		views.adicionar_comentario, name='adicionar-comentario'),
```

apps/forum/templates/detalhe-postagem-forum.hml

```html
 <form method="POST" action="{% url 'adicionar-comentario' postagem.slug %}">
```

### **Lista de Comentários**

Já temos a maior parte configurada, podemos usar **`reletad_name`** para buscar os comentarios relacionados com a postagem. Exemplo: **`postagem.postagem_comentario.all`** Na tabela de Comentarios tem um campo postagem com **related_name=postagem_comentario.** Assim temos todos os comentarios relacionados com as postagem.

```html
{% for comentario  in postagem.postagem_comentario.all %}
```

**Preparei um template aqui com as classes do bootstrap. Bem simples. Ficou bem legal.**

Criei uma pasta comentarios e dentro dela um arquivo chamado lista-comentario. Pra ficar mais facil vou tratar as coisas separadamente pra vocês entender ok.

apps/forum/templates/comentarios/lista-comentario.html

```python
<div class="mt-3">
	<h4>Comentários</h4>
	<p>Total de Comentários: {{ postagem.postagem_comentario.all|length }}</p>
	{% for comentario  in postagem.postagem_comentario.all %}
	<div class="d-flex mt-4"> 
	    <div class="bg-light border rounded-3 w-100 p-3">
	        <div class="d-flex justify-content-between">  
	            <div>
	                <img src="{{comentario.usuario.perfil.foto.url}}" class="rounded-circle mr-2" width="30" height="30"> 
	                <strong class="fst-italic">
										{{comentario.usuario.first_name}} {{comentario.usuario.last_name}}</strong>
	            </div>  
	            <span class="mx-3 fst-italic">{{comentario.data_criacao}}</span> 
	        </div> 
	        <p class="text-break mx-3 mt-3">{{comentario.comentario}}</p> 
	        <div class="d-flex justify-content-start">  
	            {% if request.user == comentario.usuario %}
	            <a href="#" class="link-success"><i class="fas fa-edit mx-2"></i></a>
	            <a href="#" class="link-danger"><i class="fas fa-trash fa-1x mx-1"></i></a> 
	            {% endif %}   
	            {% if user.is_authenticated %}  
	            <a href="#" class="link-secondary">
								<i class="fa fa-reply fa-1x mx-1"></i>Responder
							</a> 
	            {% endif %}   
	        </div>  
	    </div>  
	</div>
	{% endfor %}
</div>
```

Depois adiciona um include no template de detalhe da postagem.

`**{% include "comentarios/lista-comentario.html" %}**`

### **Editar Comentário**

Como já temos a lista de comentários precisamos criar uma rota para editar. Vamos adicionar essa função na views que vai receber um ID do comentário e form.

apps/forum/views.py

```python
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    message = 'Comentário Editado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.info(request, message)
            return redirect('detalhe-postagem-forum',
                            slug=comentario.postagem.slug)
    return JsonResponse({'status': message})
```

Registrar essa views para acessarmos.

apps/forum/urls.py

```python
path('editar-comentario/<int:comentario_id>/', 
		views.editar_comentario, name='editar-comentario'),
```

Onde tem a lista de comentarios vamos precisar adicionar um botão para chamar o formulário de edição.

apps/forum/templates/comentarios/lista-comentario.html

```python
<a href="#" 
	class="link-success" data-bs-toggle="collapse" 
	data-bs-target="#editarComentario{{comentario.id}}" 
	aria-expanded="false" 
	aria-controls="collapseEditarComentario"><i class="fas fa-edit mx-2"></i></a>
```

Aqui vamos criar um arquivo para colocar o formulário de edição. Estou usando bootstrap uma classe **`“collapse”`** para mostrar o formulário de edição. 

Um detalhe é esse textarea que vamos precisar colocar para carregar a informação dentro do input para editarmos.

**Documentação**: https://getbootstrap.com/docs/5.3/components/collapse/#example

```html
<textarea class="form-control" rows="3" name="comentario" id="comentario" 
	 placeholder="Escreva um comentário...">{{comentario.comentario}}</textarea> 
```

Resultado final fica assim… 

apps/forum/templates/comentarios/editar-comentario.html

```python
<!-- Editar Comentario  -->
<div class="collapse mt-2" id="editarComentario{{comentario.id}}"> 
    <form method="POST" action="{% url 'editar-comentario' comentario.id %}"> 
        {% csrf_token %}
        <textarea class="form-control" rows="3" name="comentario" id="comentario" 
            placeholder="Escreva um comentário...">{{comentario.comentario}}</textarea>  
         <div class="d-flex justify-content-between">  
            <button type="submit" class="btn">
							<i class="fas fa-save fa-1x"></i> Salvar
						</button>    
            <button class="btn btn-white-sm" type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#editarComentario{{comentario.id}}" 
                aria-expanded="false" 
                aria-controls="collapseEditarComentario">
                <i class="fas fa-times fa-1x"></i>
            </button>  
        </div>  
    </form> 
</div>
```

Depois no template do detalhes da postagens no for de comentarios adicionar.

`**{% include "comentarios/editar-comentario.html" %}**`

### **Deletar Comentáro**

Na views de deletar um comentário será bem simples, praticamente vamos receber um ID do objeto comentário e remover da base de dados. Depois retorna para postagem que estamos.

apps/forum/views.py

```python
def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    postagem_slug = comentario.postagem.slug
    comentario.delete()
    messages.success(request, 'Comentário deletado com sucesso!')
    return redirect('detalhe-postagem-forum', slug=postagem_slug)
```

apps/forum/urls.py

```python
path('deletar-comentario/<int:comentario_id>/', 
		views.deletar_comentario, name='deletar-comentario')
```

Não vamos usar AJAX por enquanto. Então preciamos criar um form no template para passar o id do comentário para view e remover.

apps/forum/templates/comentarios/lista-comentario.html

```html
<form method="POST" action="{% url 'deletar-comentario' comentario.id %}">
    {% csrf_token %}  
    <button type="submit" class="link-danger btn btn-transparent m-0 p-0">
			<i class="fas fa-trash fa-1x mx-1"></i>
		</button> 
</form>
```

lista-comentario.html

```jsx
<form id="form-remocao" method="POST" action="{% url 'deletar-comentario' comentario.id %}">
		{% csrf_token %}
		<button type="submit" class="link-danger btn btn-transparent m-0 p-0">
			<i class="fas fa-trash fa-1x mx-1"></i>
		</button>
	</form>
```

detalhe-postagem-forum.html
```jsx
{% block scripts %}
    <script> 
        document.addEventListener("DOMContentLoaded", function () {
            const formRemocao = document.getElementById("form-remocao");
    
            formRemocao.addEventListener("submit", function (event) {
                event.preventDefault(); // Impede o envio padrão do formulário
    
                const confirmacao = confirm("Tem certeza de que deseja remover o comentário?");
    
                if (confirmacao) {
                    // Se o usuário confirmar, envie o formulário
                    formRemocao.submit();
                }
            });
        });

    </script>
{% endblock scripts %}
```