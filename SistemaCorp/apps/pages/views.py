from django.shortcuts import render 
from pages.models import Blocos

# Create your views here.
def index(request):
    return render(request, 'index.html')


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