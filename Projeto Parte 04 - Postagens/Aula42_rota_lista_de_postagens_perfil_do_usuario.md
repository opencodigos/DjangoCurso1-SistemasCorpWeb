# **Rota Lista Postagem no Perfil do Usuário**

**Dev: Letícia Lima**

No perfil podemos fazer um tratamento diferente. Primeiro no template a gente prepara ele assim para ter a parte de filtro e lista de postagens.

apps/perfil/templates/perfil.html 

```html
...
<div class="container">
    <div class="row g-2 mt-5">
        <div class="col-md-4 bg-light">
            <form class="d-flex" role="search" method="GET">
                <input class="form-control me-2" type="search" 
											name="title_post" placeholder="Pesquisar..." aria-label="Search">
                <button class="btn btn-outline-dark" type="submit">Pesquisar</button>
            </form>
        </div>
        <div class="col-md-8">
            
            <!-- Coloca a lista de produtos aqui -->
    
        </div>
    </div>
</div>
```

Não vamos aproveitar a mesma views que temos em forum. **Não vai precisar por que já temos uma rota “perfil” e podemos fazer um tratamento diferente.** Mas antes queria explicar um pouco esse recurso do django que vamos utilizar.

documentação: https://docs.djangoproject.com/en/4.2/ref/models/querysets/

**Já usamos o select_related na aula de criar um perfil.**

1. **`select_related`**
O método **select_related** é usado para recuperar os objetos relacionados em uma única consulta SQL, utilizando joins para buscar os objetos relacionados na mesma consulta que recupera o objeto principal. O **select_related** é útil quando você precisa acessar os atributos dos objetos relacionados em seu código, pois eles já foram carregados antecipadamente.
2. **`prefetch_related`**
Por outro lado, o método **prefetch_related** é usado para buscar objetos relacionados em consultas separadas, mas de forma otimizada. O **prefetch_related** é útil quando você precisa acessar os objetos relacionados posteriormente e realizar operações em lote.

apps/perfil/views.py

```python
def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)
    context = {'obj': perfil}
    return render(request, 'perfil.html', context)

# no template note que vamos fazer o loop assim para pegar todas as 
# postagens relacionadas
{% for postagem in obg.user_postagem_forum.all %}
```

apps/perfil/template/perfil.html **Atualizamos para ficar assim.**

Futuramente podemos ate criar um componente com esse template. Por que vocês perceberam que estamos usando esse mesmo template na rota /forum/ da homepage ? E agora vamos repetir aqui no perfil. Só que com algumas diferenças, esse template tem os botões editar e excluir.

```python
<!-- Coloca a lista de produtos aqui -->
{% for postagem in obj.user_postagem_forum.all %}
<div class="p-3 mb-3 rounded-3 shadow-sm">
    <div class="align-items-center">
        <div class="d-flex justify-content-between">
            <h5><a href="{% url 'detalhe-postagem-forum' postagem.id %}">
							{{postagem.titulo}}</a></h5>
            <div class="div">
                {% if postagem.usuario == request.user %}
                <a class="btn btn-warning" 
										href="{% url 'editar-postagem-forum' postagem.id %}">
								<i class="fas fa-edit"></i></a>  
                <a class="btn btn-danger" data-bs-toggle="modal" 
										href="#confirmarExclusaoModal{{postagem.id}}" role="button">
											<i class="fas fa-trash"></i></a>  
                {% endif %}
            </div>
        </div>  
        <div class="text-truncate-box"> 
            <p class="text-truncate">{{postagem.descricao|truncatechars:230}}</p> 
        </div>
    </div>
    <div class="d-flex justify-content-between align-items-center">
        <div class="align-items-center">
            <small class="text-muted">{{postagem.data_publicacao}}</small>
        </div>
    </div>
</div>
{% include "modal-deletar-postagem-forum.html" %}
{% endfor %}
```

Feito isso já temos um resultado interessante. como estamos utilizando a instancia de perfil não precisa aplicar filtro para aparecer as postagens deacordo com cada usuário. **Isso ta acontecendo devido ao relacionamento.**