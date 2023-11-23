# **Rota Lista Postagens no Dashboard (Restrição de Acesso)**

**Dev: Letícia Lima**

**Dashboard**

Precisamos exibir as postagens de acordo com o usuário correto. Por exemplo, se houver uma postagem oculta de um usuário X, o usuário Y não deve ser capaz de vê-la. No entanto, os usuários **administradores ou colaboradores** devem ter permissão para visualizá-la, conforme necessário. 

Existem várias abordagens para lidar com essa situação. Neste caso, podemos aproveitar a mesma visualização para tratar essas diferenças.

Primeiro vamos usar `**print(request.path)**` na rota de `**lista_postagem_forum()**` para vermos o path da pagina de forum que lista todas as postagens ativas. Feito isso a gente sabe que `**/forum/**` deve ser a rota onde mostra todas as postagens ativas independente do usuário autenticado ou não. 

apps/forum/views.py

```python
def lista_postagem_forum(request):
    if request.path == '/forum/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html' # lista de post da rota /forum/
    else: # Essa parte mostra no Dashboard
        user = request.user 
        template_view = 'dashboard/dash-lista-postagem-forum.html' # template novo que vamos criar 
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)
    context = {'postagens': postagens}
    return render(request, template_view, context)
```

A partir do primeiro else se tiver alguma rota especifica pode ser tratada ali. como só teremos duas views para listar essas postagens então achei mais simples tratar desse jeito.

Feito isso vamos criar uma nova rota no urls. 

```python
path('dashboard/lista-postagem/', views.lista_postagem_forum, name='dash-lista-postagem-forum'), 
```

**O template vamos tratar assim. Vamos criar um novo template somente para essa lista que vamos ter no dashboard.**

Utilizando as classe bootstrap podemos fazer uma tabelinha assim. Lembra quando criamos o modal para deletar uma postagem e colocar assim **`#confirmarExclusaoModal{{postagem.id}}`  para não termos problemas quando for uma lista assim.** **Para cada objeto tera um modal relacionado com mesmo.**

apps/forum/templates/dashboard/dash-lista-postagem-forum.html

```html
{% extends 'base_dashboard.html' %}
{% block title %}Dashboard - Lista de Postagens{% endblock %}
{% block content_dash %}
<div class="p-3">
    <div class="d-flex justify-content-between mb-3">
        <button class="btn btn-secondary" onclick="location.href='{% url 'criar-postagem-forum' %}'">
            <i class="fas fa-user mx-2"></i> + Criar Postagem</button>
        <h2>Todas as Postagens </h2>
    </div>
    <!-- table -->
    <div class="table-responsive">
        <table class="table table-light">
            <thead class="table-light">
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Nome/Sobrenome</th>
                    <th scope="col">Titulo</th>
                    <th scope="col">Data Criação</th>
                    <th scope="col">Data Publicação</th>
                    <th scope="col">Ativo</th>
                    <th scope="col">Acão</th>
                </tr>
            </thead>
            {% for postagem in postagens %}
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
                        <a class="link-warning" href="{% url 'detalhe-postagem-forum' postagem.id %}"><i class="fas fa-eye mx-2"></i></a>
                        <a class="ml-2 link-secondary" href="{% url 'editar-postagem-forum' postagem.id %}"><i class="far fa-file mx-2"></i></a>
                        <a class="ml-3 link-danger" data-bs-toggle="modal" href="#confirmarExclusaoModal{{postagem.id}}" role="button"><i class="fas fa-trash mx-2"></i></a>
                        {% include "deletar-postagem-forum.html" %}
                    </td>
                </tr>
            </tbody>
            {% empty %}
            <p>Nenhuma poste cadastrado.</p>
            {% endfor %}
        </table>
    </div>
</div>
{% endblock %}
```

Se acessarmos a rota: http://localhost:8000/forum/dashboard/lista-postagem/ Já vamos ter o resultado.

No dashboard temos um item no menu lateral chamado **“Relatórios”** vamos criar um bloco para chamar esse tipo de relatório.

### **Então no app config.**

apps/config/views.py

```python
@login_required
def relatorio_view(request):
    return render(request, 'relatorio.html')
```

apps/config/urls.py

```python
path('relatorio/', views.relatorio_view, name='relatorio'),
```

De inicio vou usar esse layout feito com bootstrap. É bloco que redireciona para a lista de postagens. 

Depois mais pra frente podemos automatizar essa parte, quando for fazer melhorias no codigo. *(hehehe se preparem)*

apps/config/template/relatorio.html

```html
{% extends 'base_dashboard.html' %}
{% block title %}Relatórios{% endblock %}
{% block content_dash %} 
<div class="row row-cols-1 row-cols-md-3 g-4"> 
	
	<div class="col" style="width: 25rem;">   
		<div class="card h-100 border-0 bg-white shadow-sm">
			<div class="card-body py-5 text-center">
				<h2 class="card-title">Postagens</h2>
				<p class="card-text">Lista de Postagens</p>
			</div>
			<div class="d-grid col-10 mx-auto p-5">  
				<button class="btn btn-info btn-lg w-100" 
					onclick="location.href='{% url 'dash-lista-postagem-forum' %}'">
					Acessar</button> 
			</div>
		</div> 
	</div> 
	...
	<!-- Outros -->
	
</div>
{% endblock %}
```

Agora para finalizar precisamos atualizar no dashboard base a rota.

Outro menu que podemos automatizar mais pra frente.

apps/base/template/base_dashboard.html
```python
<button type="button" class="btn btn-light" onclick="location.href='{% url 'relatorio' %}'">
                <i class="fas fa-file-alt me-2"></i>Relatórios</button>
```