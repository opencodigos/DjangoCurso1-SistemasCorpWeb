# **Aprovar Usuário no Sistema**

**Dev: Letícia Lima**

Vamos supor que seja um sistema fechado. Não é qualquer cliente ou usuario que pode acessar a plataforma. Então seria interessante ter um usuario administrador para aprovar o registro do usuário recem cadastrado. Atualmente funciona da seguinte forma, qualquer usuario pode se inscrever. Como a gente pode limitar isso.

**No modelo MyUser está `is_active = models.BooleanField(default=True)` então qualquer conta criada o estará automaticamente como true.** 

é Simples, Na view de ***register_view*** podemos setar um campo ***is_active*** para False. E precisamos avisar o cliente/usuario que o cadastro dele será aprovado por um administrador. Esse aviso pode ser um popup na tela ou e-mail. Eu prefiro o contato por e-mail. por que fica registrado. Popup some da tela, usuario finge que não vê, é muito ruim. 

Depois que usuário for aprovado para usar a plataforma. Temos que avisar o usuário que ele foi aprovado, esse aviso será por e-mail tambem.

Primeiro no na função `**def register_view(request):**` adicionamos:

```python
def register_view(request):
	if form.is_valid():
    ...
    usuario.is_active = False # Adiciona isso.
    usuario.save() 
	  ...
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
```

E quando um usuário for alterado podemos fazer a validação e enviar e-mail. Nessa rota aqui.

```python
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
```