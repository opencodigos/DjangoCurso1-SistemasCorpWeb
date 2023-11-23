# Paginação

**Dev: Letícia Lima**

### Lista Postagem (Forum)

Doc: https://docs.djangoproject.com/pt-br/4.2/topics/pagination/

Vamos precisar mexer um pouco da função de lista de postagem. Estamos fazendo esse tratamento diferente só por causa do modal, pois temos um formulário de edição no modal. Mas fora isso deve ficar igual o que está na documentação. 

apps/forum/views.py

```python
from django.core.paginator import Paginator

def lista_postagem_forum(request):
    form_dict = {}
    if request.path == '/forum/':
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html'
    else:
        user = request.user
        template_view = 'dashboard/dash-lista-postagem-forum.html'
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            postagens = models.PostagemForum.objects.filter(usuario=user)
        
    for el in postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)
```

apps/base/templates/components/paginacao.html

```html
<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">Primeiro</a>
            <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Proximo</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">Ultima</a>
        {% endif %}
    </span>
</div>
```

No template precisamos fazer algumas mudanças. Por exemplo agora vamos adicionar form_dict.items na rota de lista postagem da home e incluir o componente de paginação generico que criamos.

**apps/forum/templates/lista-postagem-forum.html
apps/forum/templates/dash-lista-postagem-forum.html**

```html
...
		{% for postagem, form in form_dict.items %}

		{% endfor %}
    </div> 
</div>
{% include 'components/paginacao.html' %}
...
```

**Aplicando classes boostrap pra ficar bunitinho!!!**

DOC: https://getbootstrap.com/docs/5.3/components/pagination/

apps/base/templates/components/paginacao.html

```html
<div class="pagination">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page=1">&laquo; Primeira</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Anterior</a>
        </li>
        {% endif %}
        <li class="page-item active">
            <span class="page-link">
            {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}
            </span>
        </li>
        {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Proximo</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Ultima &raquo;</a>
            </li>
        {% endif %}
    </ul>
</div>
```

**Para mudar a cor.**

apps/base/statics/css/styles.css

```python
.pagination .page-link {
    background: rgb(138, 138, 138);
    color: white;
    border: none;
}
```

### Lista de Usuários (Contas)

apps/contas/views.py

```python
from django.core.paginator import Paginator

@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request):
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False)
    paginacao = Paginator(lista_usuarios, 3)
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    context = {'page_obj': page_obj}
    return render(request, 'lista-usuarios.html', context)
```

apps/contas/lista-usuarios.html

```python
...
{% for usuario in lista_usuarios %}
<tbody>

...
</table>
</div>
{% include 'components/paginacao.html' %}
```

### Lista de Postagem (Perfil)

apps/perfil/views.py

```python
from django.core.paginator import Paginator

def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)
    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
    
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'perfil.html', context)
```

apps/perfil/templates/perfil.html

```python
						 ...
            {% endfor %}
            {% include 'components/paginacao.html' %} # Adciona paginacao
        </div>
    </div>
</div>
```

Estamos usando o mesmo context **page_obj** por conta do template generico da paginação. Isso pode ser tratado por app. Você pode criar um template de paginação para cada app. Nosso caso aqui não será necessario, paginação é um componente que não teremos problemas em aproveitar em outras views.

Os que tem o form_dict o dicionario a gente adiciona page_obj como mais um contexto para usar. Vai da certo.