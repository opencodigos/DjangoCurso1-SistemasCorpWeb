from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
def timeout_view(request):
    return render(request, 'timeout.html')


def login_view(request):
    if request.method == 'POST': # metodo POST
        email = request.POST.get('email') # Valor do campo email
        password = request.POST.get('password') # Valor do campo password 
        user = authenticate(request, email=email, password=password) # Retorna a autenticação
        if user is not None: # se user não for none ou underfine 
            login(request, user) # faz login no sistema
            return redirect('home') # Volta para rota home 
        else:
            messages.error(request, 'Email ou senha inválidos') # senão, retorna mensagem de erro
    if request.user.is_authenticated: # se usuario acessar a rota /login, já estiver autenticado retorna para home
        return redirect('home')
    return render(request, 'login.html')