from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from forum.forms import PostagemForumForm
from django.contrib import messages  
from forum import models


# Lista de Postagens.
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True)
    context = {'postagens': postagens}
    return render(request, 'lista-postagem-forum.html', context)


# Cria postagens 
def criar_postagem_forum(request): 
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user
            forum.save()
            # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
            messages.success(request, 'Seu Post foi cadastrado com sucesso!')
            return redirect('lista-postagem-forum')
    return render(request, 'form-postagem-forum.html', {'form': form})


# Detalhes da postagem
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem})


# Edtar Postagem
@login_required
def editar_postagem_forum(request, id):
    lista_grupos = ['administrador', 'colaborador']
    postagem = get_object_or_404(models.PostagemForum, id=id) 
    
    # Verifica se o usuário autenticado é o autor da postagem
    if request.user != postagem.usuario and not (
        any(grupo.name in lista_grupos for grupo in user.groups.all()) or request.user.is_superuser):
            return redirect('postagem-forum-list')  # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Seu Post '+ postagem.titulo +' \
                foi atualizado com sucesso!')
            return redirect('editar-postagem-forum', id=postagem.id)
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = PostagemForumForm(instance=postagem)
    return render(request, 'form-postagem-forum.html', {'form': form})


# Deletar Postagem
@login_required 
def deletar_postagem_forum(request, id): 
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, 'Seu Post '+ postagem.titulo +' foi deletado com sucesso!')
        return redirect('lista-postagem-forum')
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem})


# Lista de Postagens no Dashboard (Gerenciar)
def lista_postagem_forum(request):
    if request.path == '/forum/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html' # lista de post da rota /forum/
    else: # Essa parte mostra no Dashboard
        user = request.user 
        lista_grupos = ['administrador', 'colaborador']
        template_view = 'dashboard/dash-lista-postagem-forum.html' # template novo que vamos criar 
        if any(grupo.name in lista_grupos for grupo in user.groups.all()) or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)
    context = {'postagens': postagens}
    return render(request, template_view, context)