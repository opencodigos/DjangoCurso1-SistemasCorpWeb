from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def index(request):
    # messages.success(request, "Operação realizada com sucesso!")
    # messages.error(request, "Ocorreu um erro!")
    # messages.warning(request, "Atenção com esta ação.")
    # messages.info(request, "Essa é uma informação.")
    return render(request, 'index.html')