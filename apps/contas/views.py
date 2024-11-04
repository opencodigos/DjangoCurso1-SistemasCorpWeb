from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group 
from django.contrib.auth.forms import PasswordChangeForm 
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from contas.models import MyUser
from contas.forms import CustomUserCreationForm, UserChangeForm
from contas.permissions import grupo_colaborador_required
from perfil.models import Perfil
from perfil.forms import PerfilForm

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
        if user is not None:
            login(request, user)
            
            if user.is_authenticated and user.requires_password_change(): # Verifica
                msg = 'Olá '+user.first_name+', como você pode perceber atualmente \
                        a sua senha é 123 cadastrado. Recomendamos fortemente \
                        que você altere sua senha para garantir a segurança da sua conta. \
                        É importante escolher uma senha forte e única que não seja fácil de adivinhar. \
                        Obrigado pela sua atenção!' 
                messages.warning(request, msg)
                return redirect('force_password_change') # Vai para rota de alterar senha.
            else:
                return redirect('home')
            
        else:
            messages.error(request, 'Email ou senha inválidos') # senão, retorna mensagem de erro
    if request.user.is_authenticated: # se usuario acessar a rota /login, já estiver autenticado retorna para home
        return redirect('home')
    return render(request, 'login.html')


# Registrar um usuário
def register_view(request):
    if request.method == "POST": # metodo POST
        form = CustomUserCreationForm(request.POST, user=request.user) # Formulário que criamos no forms.py
        if form.is_valid(): # se formulário for valido registra usuário
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.is_active = False # Adiciona isso. 
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            Perfil.objects.create(usuario=usuario) # Cria instancia perfil do usuário
             
            # Envia e-mail para usuário
            send_mail( # Envia email para usuario
                'Cadastro Plataforma',
                f'Olá, {usuario.first_name}, em breve você receberá um e-mail de \
                    aprovação para usar a plataforma.',
                'email@email.com', # De (em produção usar o e-mail que está no settings)
                [usuario.email], # para
                fail_silently=False,
            )
            
            messages.success(request, 'Registrado. Um e-mail foi enviado \
                para administrador aprovar. Aguarde contato')
            
            return redirect('login') # Redireciona para login
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm(user=request.user) # Inicialmente carrega o formulário no template, os campos etc..
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
def atualizar_usuario(request, username):
    user = get_object_or_404(MyUser, username=username)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            usuario = form.save()
             
            if user.is_active: ## se usuario for ativado a gente muda o status para True e envia e-mail
                usuario.is_active = True # muda status para True (Aprovado)
                print(usuario.is_active)
                # Envia e-mail avisando usuário.
                send_mail( # Envia email para usuario
                    'Cadastro Aprovado',
                    f'Olá, {usuario.first_name}, seu e-mail foi aprovado na plataforma.',
                    settings.DEFAULT_FROM_EMAIL, # De (em produção usar o e-mail que está no settings)
                    [usuario.email], # para
                    fail_silently=False,
                )
                messages.success(request, 'O usuário '+ usuario.email +'\
                    foi atualizado com sucesso!')
                return redirect('lista_usuarios')
            
            usuario.save()   
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})


# Lista de usuário cadastrado no sistema. 
# Somente admin e colab pode ser essa lista
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request): # Lista Cliente 
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False) 
    return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})


# Adicionar usuário no sistema, somente admin e colab podem cadastrar.
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def adicionar_usuario(request):
    user_form = CustomUserCreationForm(user=request.user)
    perfil_form = PerfilForm(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, user=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, user=request.user)

        if user_form.is_valid() and perfil_form.is_valid():
            # Salve o usuário
            usuario = user_form.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            # Crie um novo perfil para o usuário
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
 
            messages.success(request, 'Usuário adicionado com sucesso.')
            return redirect('lista_usuarios')
        else:
            for field, error_list in user_form.errors.items():
                for error in error_list:
                    messages.error(request, f"Error no campo '{user_form[field].label}': {error}")
            
            for field, error_list in perfil_form.errors.items():
                for error in error_list:
                    messages.error(request, f"Error no campo '{perfil_form[field].label}': {error}") 
            
            # Error
            # error_list1 = user_form.errors.as_text()
            # error_list2 = perfil_form.errors.as_text()
            # # Voce pode fazer o que quiser com a lista de erros 
            # messages.error(request, error_list1)
            # messages.error(request, error_list2)
            
    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, "adicionar-usuario.html", context)
 

# Mudança de Senha Force (first_login)
@login_required
def force_password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_change_password = False # passa o parametro para False.
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'registration/password_force_change_form.html', context)