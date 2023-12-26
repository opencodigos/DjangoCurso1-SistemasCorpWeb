# **Multiplos Anexos na Postagem (Bonus)(Deletar Imagem)**

Dev: Letícia Lima

### Deletar Imagem do Anexo

Vamos usar Ajax para fazer isso, Eu não queria usar ajax ainda nesse inicio, masss !!! seria interessante vocês ve como pode ser simples usar ajax e deixar as coisas mais dinamicas. Basicamente vamos criar uma função que só remove a imagem ( Anexo ) com base no parametro que vamos requisitar.

apps/forum/views.py

```python
def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.PostagemForumImage.objects.filter(id=imagem_id) # Filtra pra ver se imagem existe...
    if verifica_imagem:
        postagem_imagem = models.PostagemForumImage.objects.get(id=imagem_id) # pega a imagem
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        postagem_imagem.imagem.delete()
        postagem_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso.'})
```

apps/forum/urls.py

```python
# AJAX
path('remover-imagem/', views.remover_imagem, name='remover-imagem'),
```

No template vamos modificar 2 coisas. Primeiro precisamos passar para rota de deletar o Id da imagem. 

apps/forum/template/modal-form-postagem-forum.html

```html
<div class="d-flex g-3">
{% for img in postagem.postagem_imagens.all %}
	<div class="position-relative p-2 div-imagem">
		<a href="#" class="position-absolute badge bg-danger remover-imagem" data-imagem-id="{{img.id}}">
			<i class="fas fa-times"></i>
		</a>
		<img src="{{ img.imagem.url }}" class="img-fluid rounded" alt="{{img.id}}" width="100"> 
	</div>
{% endfor %}
</div>
```

`**div-imagem` Tenho um bloco representa a imagem completa.**

`**remover-imagem` Class apenas para usar no ajax no Click**

**`data-imagem-id` É o atributo que ta recebendo um valor no caso o id da imagem.**

```jsx
<script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>
<script>
	$('.remover-imagem').click(function(e) {
		e.preventDefault();
		var imageId = $(this).data('imagem-id'); // Aqui vai retorna o id da imagem
		$.ajax({
			type: 'GET',
			url: '{% url "remover-imagem" %}',
			data: {'imagem_id': imageId}, // Envia para rota onde deleta a imagem
			datatype: "json",
			success: function (data) { // vamos ter um reforno
				// Remover a div da imagem do DOM
				$(e.target).closest('.div-imagem').remove(); // No template removo essa imagem. Trata no frontend.
			}, 
		});
	});
</script>
```

Legal. Testem ai. é para funcionar na rota Perfil/dashboard/Detalhes
