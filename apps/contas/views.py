from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group 
from django.shortcuts import render, redirect, get_object_or_404
from contas.models import MyUser
from contas.forms import CustomUserCreationForm, UserChangeForm
from contas.permissions import grupo_colaborador_required

# Timeout (1hora)
def timeout_view(request):
    return render(request, 'timeout.html')
 
 
# Logout (Sair do sistema)
def logout_view(request):
    logout(request)
    return redirect('home')


# Autenticar um usuario
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


# Registrar um usuário
def register_view(request):
    if request.method == "POST": # metodo POST
        form = CustomUserCreationForm(request.POST) # Formulário que criamos no forms.py
        if form.is_valid(): # se formulário for valido registra usuário
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            
            return redirect('login') # Redireciona para login
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm() # Inicialmente carrega o formulário no template, os campos etc..
    return render(request, "register.html",{"form": form})


# Atualizar usuario autenticado (meu usuario)
@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})


# Atualizar usuário passa um parametro ID de qualquer usuario
@login_required()
@grupo_colaborador_required(['administrador','colaborador'])
def atualizar_usuario(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})