# **Multiplos Anexos na Postagem (Bonus)** (Criar Postagem)

Dev: Letícia Lima

### Rota Criar Postagem

Feito isso vamos criar o forms para implementar no nosso modal.

<aside>
⚠️ **Para fazer upload de multiplos arquivos vamos usar uma biblioteca nativa do proprio django. Unico problema desse metodo é que só funciona na versão atualizada do Django. A partir da 4.2. As versão anteriores usa um parametro diferente.**

</aside>

Doc: [https://docs.djangoproject.com/en/4.2/topics/http/file-uploads](https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/)

Com base na documentação vamos começar modificando nosso forms para tratar o campo a receber multiplos arquivos.

apps/forum/forms.py

```python
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
				widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}))
    postagem_imagens = MultipleFileField(
				label='Selecione no máximo 5 imagens.',required=False) # Adiciona isso

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo'] # remove anexar imagem

```

### Rota Criar Postagem

Na função `**criar_postagem_forum**` vamos precisar fazer um getList para pegar as imagens uma por uma e salvar na tabela relacionada que criamos anteriormente. Esse **“postagem_imagens”** é o nome do relacionamento que definimos no modelo e colocamos no forms. Tem que ser igual ok. Depois fazemos um for para salvar as imagens no modelo.

apps/forum/views.py

```python
def criar_postagem_forum(request):
	...      
	forum = form.save(commit=False)
	forum.usuario = request.user
	forum.save()
	
	postagem_imagens = request.FILES.getlist('postagem_imagens')
	for f in postagem_imagens:
	    models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
	# Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
	messages.success(request, 'Seu Post foi cadastrado com sucesso!')
	return redirect('lista-postagem-forum')
	...
```

**Conseguimos testar e verificamos que está salvando multiplas imagens. O problema é que estamos conseguindo salva mais de 5 anexos. Isso significa que precisamos tratar essa regra.** 

Pega a quantidade de Arquivos no anexo e faz um *count* antes de salvar. E coloca um *If* pra verificar. 

apps/forum/views.py

```python
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens') # pega as imagens
            if len(postagem_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                forum = form.save(commit=False)
                forum.usuario = request.user
                forum.save()
                for f in postagem_imagens:
                    models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                return redirect('lista-postagem-forum')
    return render(request, 'form-postagem-forum.html', {'form': form})
```

Agora para visualizar esses anexos no template, vamos modificar o tratamento que fizemos antes na rota Detalhes da postagem.

apps/forum/templates/detalhe-postagem-forum.html
```python
{% for imagem in postagem.postagem_imagens.all %} # Adiciona um for 
<a data-bs-toggle="modal" href="#imagemModal{{imagem.id}}" role="button"><i class="link-info fas fa-image fa-2x me-2"></i></a>
<div class="modal fade" id="imagemModal{{imagem.id}}" tabindex="-1" aria-labelledby="imagemModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="imagemModalLabel"><i class="link-info fas fa-image fa-2x me-2"></i></h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body"> 
                <img src="{{ imagem.imagem.url }}" alt="Imagem da postagem" class="img-fluid">
            </div> 
        </div>
    </div>
</div>  
{% endfor %}
```