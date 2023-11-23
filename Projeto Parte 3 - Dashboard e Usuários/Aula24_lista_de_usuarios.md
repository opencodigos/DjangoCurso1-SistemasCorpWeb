# **Lista de Usuários**

Vamos criar uma lista de usuário, na nossa view chamando o todos os usuarios de MyUser e tabela relacionada perfil para pegar as informações. E um filtro is_superuser=False para não aparecer os super usuarios.

Estamos tratando na view para que somente perfil administrador e colaborador possa acessar essa rota. Usuário padrão não pode. Depois tratamos no template para não aparecer esse menu.

apps/contas/views.py

```python
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request): # Lista Cliente 
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False) 
    return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})
```

apps/contas/urls.py

```python
path('lista-usuarios/', views.lista_usuarios, name='lista_usuarios'),
```

apps/contas/templates/lista-usuarios.html

```html
{% extends 'base_dashboard.html' %}
{% block title %}Lista Usuários{% endblock %}
{% load static %}
{% block content_dash %}
<div class="p-3">

	<div class="d-flex justify-content-between mb-3">
		<button class="btn btn-secondary" onclick="window.location.href='#'">
			<i class="fas fa-user mx-2"></i> Adicionar Novo</button>
		<h2>Todas usuários cadastrados no sistema</h2>
	</div>

	<!-- table -->
	<div class="table-responsive">
		<table class="table table-light">
			<thead class="table-light">
				<tr>
					<th scope="col">#</th>
                    <th scope="col">Foto</th>
					<th scope="col">Nome/Sobrenome</th>
					<th scope="col">E-mail</th>
					<th scope="col">Data Criação</th>
					<th scope="col">Ativo</th>
					<th scope="col">Acão</th>
				</tr>
			</thead>
			{% for usuario in lista_usuarios %}
			<tbody>
				<tr>
                    <td scope="row">{{ usuario.id }}</td>
                    <td scope="row">
                        {% if usuario.perfil.foto %}
                        <img src="{{usuario.perfil.foto.url}}" class="img-thumbnail border rounded" width="30" alt="">  
                        {% else %}
                        <img src="{% static 'images/perfil/foto-padrao.jpg' %}" class="img-thumbnail border rounded" width="30" alt="">
                        {% endif %}
                    </td>
					<td scope="row">{{ usuario.first_name }} {{ usuario.last_name }}</td>
					<td scope="row">{{ usuario.email }}</td>
					<td scope="row">{{ usuario.date_joined|date:'d/m/Y'}}</td>
					<td scope="row">
						{% if usuario.is_active %}
						<span class="badge bg-success rounded-pill d-inline">Ativado</span> 
						{% else %}
						<span class="badge bg-danger rounded-pill d-inline">Desativado</span>  
						{% endif %}
					</td>
					<td scope="row">
						<a class="link-warning" href=""><i class="fas fa-eye mx-2"></i></a>
						<a class="ml-2 link-secondary" href="{% url 'atualizar_usuario' usuario.username %}"><i class="far fa-file mx-2"></i></a>
						<a class="ml-3 link-danger" href=""><i class="fas fa-trash mx-2"></i></a>
					</td>
				</tr>
			</tbody>
			{% empty %}
			<p>Nenhuma usuário cadastrado.</p>
			{% endfor %}
		</table>
	</div>
</div>
{% endblock %}
```

apps/base/templates/base_dashboard.html

```python
<button type="button" class="btn btn-light" onclick="location.href='{% url 'lista_usuarios' %}'">
                <i class="fas fa-users me-2"></i>Usuários do Sistema</button>
```

Se quiser pode adicionar nas configurações de conta tambem. 

`<li><a href="{% url 'lista_usuarios' %}">Lista Todos usuários</a></li>`

**Podemos até adicionar uma regra no template para trabalhar com permissões.**

app contas e a permissão de contas.view_myuser. Significa que somente usuarios com a permissão para acessar pode ver esse botão no template. 

Doc: https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions

exemplo:
```python
{% if perms.contas.view_myuser %}
<button type="button" class="btn btn-light" onclick="location.href='{% url 'lista_usuarios' %}'">
                <i class="fas fa-users me-2"></i>Usuários do Sistema</button>
{% endif %}
```