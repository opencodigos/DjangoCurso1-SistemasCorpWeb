from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def painel_view(request):
    return render(request, 'painel.html')

@login_required
def configuracao_view(request):
    return render(request, 'configuracao.html')

@login_required
def relatorio_view(request):
    return render(request, 'relatorio.html')