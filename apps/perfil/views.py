from django.shortcuts import get_object_or_404, render
from contas.models import MyUser

def perfil_view(request, id):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), id=id)
    context = {'obg': perfil}
    return render(request, 'perfil.html', context)