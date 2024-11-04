from django.shortcuts import get_object_or_404, render
from contas.models import MyUser
from forum.forms import PostagemForumForm

def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)

    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form

    return render(request, 'perfil.html', {'obj': perfil,'form_dict':form_dict})