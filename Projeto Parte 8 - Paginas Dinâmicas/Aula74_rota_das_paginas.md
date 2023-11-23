# **Rota das Paginas**

Dev: Letícia Lima

 

Como vamos tratar isso na view. Um jeito simples e clean seria criar uma unica função e tratar. 

Esse paramento vai retornar o name da url. Assim conseguimos tratar a exibição dos blocos em paginas diferentes. Depois tenho um dict simples com as 4 paginas que temos. home, sobre, faq e contato, e de acordo com a pagina que acessarmos obteremos o contexto para exibir certo ?

`url_name = request.resolver_match.url_name`

apps/pages/views.py

```python
def paginas_view(request):
    url_name = request.resolver_match.url_name
    pagina = {
        'home': Blocos.objects.filter(pagina__nome='inicio',ativo=True).order_by('ordem'),
        'sobre': Blocos.objects.filter(pagina__nome='sobre',ativo=True).order_by('ordem'),
        'faq': Blocos.objects.filter(pagina__nome='faq',ativo=True).order_by('ordem'),
        'contato': Blocos.objects.filter(pagina__nome='contato',ativo=True).order_by('ordem'),
        }
    context = {'blocos': pagina[str(url_name)]}
    return render(request, 'index.html', context)
```

as todas ficam assim.

apps/pages/urls.py
```python
from django.urls import path 
from pages import views

urlpatterns = [
    path('', views.paginas_view, name='home'), 
    path('sobre/', views.paginas_view, name='sobre'), 
    path('faq/', views.paginas_view, name='faq'), 
    path('contato/', views.paginas_view, name='contato'), 
]
```