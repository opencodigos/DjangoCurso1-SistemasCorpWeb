# **Rota Detalhe Postagem**

**Dev: Letícia Lima**

Para ver os detalhes da postagem vamos adicionar uma função na view que vai receber um id da postagem e mostrar os dados.

apps/forum/views.py

```python
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem})
```

apps/forum/urls.py

```python
path('detalhe-postagem-forum/<int:id>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
```

O template para visualizar uma postagem inicialmente vamos herdar de **base.html**. São postagens ativas que vão aparecer na rota forum. Então inicialmente o template fica assim.

apps/forum/templates/detalhe-postagem-forum.html

```html
{% extends "base.html" %}
{% block title %}Detalhes da Postagem{% endblock %}
{% block content %}
<div class="container mt-3">
    <div class="row">
        <div class="col-md-8"> 
            <div class="bg-light p-3">  
                <div class="d-flex justify-content-between">
                    <span>{{postagem.data_publicacao}}</span><br> 
                    <div class="div"> 
                        <a class="btn btn-warning" href="#"><i class="fas fa-edit"></i></a>  
                        <a class="btn btn-danger" href="#"><i class="fas fa-trash"></i></a>
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
{% endblock %}
```

Já temos a rota de visualizar uma postagem. Portando podemos adicionar a url de redirecionamento no link dos card que fica na lista de postagens.

apps/forum/templates/lista-postagem-forum.html
```python
<h5><a href="{% url 'detalhe-postagem-forum' postagem.id %}">{{postagem.titulo}}</a></h5>
```