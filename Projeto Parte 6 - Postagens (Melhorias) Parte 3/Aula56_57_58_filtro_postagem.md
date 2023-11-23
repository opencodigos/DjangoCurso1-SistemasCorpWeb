# **Filtro Postagem**

Dev: Letícia Lima

**Vamos adicionar um campo para pesquisar as postagens por titulo.**

Primeiro filtro será na navbar onde temos um input tipo text para pesquisar por titulo por exemplo. Ai vamos passar parametro para url e fazer o filtro.

**Segue alguns links da documentação no Django Sobre filtro e tags.**

https://docs.djangoproject.com/en/4.2/ref/templates/builtins/

https://docs.djangoproject.com/en/4.2/ref/models/querysets/

https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/

Primeiro vamos criar uma função genericar e usarmos para filtro. Vou criar um base mesmo. Por que seria uma função generica, pode ser usada com qualquer aplicação e modelo. 

apps/base/filtros.py

```python
def filtrar_modelo(modelo, **filtros):
    queryset = modelo.objects.all()
    for campo, valor in filtros.items():
        lookup = f"{campo}__icontains"
        queryset = queryset.filter(**{lookup: valor})
    return queryset
```

apps/forum/views.py

```python
from base.filtros import filtrar_modelo

def lista_postagem_forum(request):
    form_dict = {}
    filtros = {}

    titulo_busca = request.GET.get("titulo")
    if titulo_busca:
        filtros["titulo"] = titulo_busca
		...
		else:
		...
		postagens = filtrar_modelo(models.PostagemForum, **filtros)
    ...
```

apps/base/templates/components/navbar.html

```html
<input type="search" name="titulo" class="form-control me-2" placeholder="Buscar por título" 
	aria-label="Search" value="{{ request.GET.titulo }}">
```

apps/forum/templates/dash-lista-postagem-forum.html

```python
<div class="d-flex justify-content-between mb-3">
  <div class="hstack gap-3">

      <button class="btn btn-secondary" onclick="location.href='{% url 'criar-postagem-forum' %}'">
          <i class="fas fa-user mx-2"></i> + Criar Postagem</button>
      
      <form class="hstack gap-1" method="GET" action="?">
          <input type="text" name="titulo" class="form-control" placeholder="Buscar por título" 
              value="{{ request.GET.titulo }}">
          <!-- Outros campos de filtro aqui, se necessário -->
          <button class="btn btn-outline-secondary" type="submit"><i class="fas fa-search"></i></button>
          {% if request.GET.titulo %}
          <a href="{% url 'dash-lista-postagem-forum' %}" class="link-secondary">Resetar</a>
          {% endif %}
      </form>

  </div> 
  <h2>Todas as Postagens </h2>
</div>
```

```jsx
from django.db.models import Q

# Filtro (OR)
def filtrar_modelo(modelo, **filtros):
    queryset = modelo.objects.all()
    
    q_objects = Q()  # Inicializa um objeto Q vazio

    for campo, valor in filtros.items():
        q_objects |= Q(**{campo + '__icontains': valor})

    queryset = queryset.filter(q_objects)
    return queryset
```

### Lista de Postagens no Perfil

apps/perfil/views.py 

```python
from base.utils import filtrar_modelo

def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)
    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas com perfil
    form_dict = {}
    filtros = {} # Filtro dict

    titulo_busca = request.GET.get("titulo") # Pego parametro
    if titulo_busca:
        filtros["titulo"] = titulo_busca # Adiciono no dicionario
        
    # Utiliza o modelo das postagens do perfil
    perfil_postagens = filtrar_modelo(perfil_postagens.model, **filtros) # Faz o filtro
		
		for el in perfil_postagens:
    ...
```

apps/perfil/templates/perfil.html

```html
<form class="hstack gap-1" method="GET" action="?">
    <input type="text" name="titulo" class="form-control" placeholder="Buscar por título" 
        value="{{ request.GET.titulo }}">
    <!-- Outros campos de filtro aqui, se necessário -->
    <button class="btn btn-outline-secondary" type="submit"><i class="fas fa-search"></i></button>
    {% if request.GET.titulo %}
    <a href="{% url 'perfil' obj.username %}" class="link-secondary">Resetar</a>
    {% endif %}
</form>
```

**É possivel trabalhar com varios parametros tambem. por exemplo** 

```python
titulo_busca = request.GET.get("titulo")
autor_busca = request.GET.get("autor")
categoria_busca = request.GET.get("categoria")
data_inicio = request.GET.get("data_inicio")
data_fim = request.GET.get("data_fim")
ativo = request.GET.get("ativo")

if titulo_busca:
    filtros["titulo__icontains"] = titulo_busca

if ativo :
    filtros["ativo"] = ativo

if autor_busca:
    filtros["autor__icontains"] = autor_busca

if categoria_busca:
    filtros["categoria__icontains"] = categoria_busc

if data_inicio and data_fim:
    filtros["data_publicacao__range"] = [data_inicio, data_fim]
```

Nesse exemplo, adicionei mais dois parâmetros de filtro além do título: **`autor_busca`** e **`categoria_busca`**. Se esses parâmetros estiverem presentes nos parâmetros da URL, eles serão adicionados ao dicionário de filtros correspondente aos campos "autor" e "categoria".

Dessa forma, você pode adicionar quantos parâmetros de filtro desejar ao dicionário **`filtros`** e a função **`filtrar_modelo`** aplicará todos eles no modelo. Certifique-se de ajustar os nomes dos campos no dicionário de filtros de acordo com os campos reais do modelo que deseja filtrar.