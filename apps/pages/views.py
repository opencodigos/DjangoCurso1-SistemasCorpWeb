from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
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


@csrf_exempt
def enviar_contato(request):
    if request.method == "POST": # Pega os valores do formulário
        data = json.loads(request.body)
        nome = data.get('nome')
        email = data.get('email')
        titulo = data.get('titulo')
        mensagem = data.get('mensagem')

        if not all([nome, email, titulo, mensagem]): # Valida se todos estão preenchidos
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)

        try:
            send_mail( # Usa send_mail lib para enviar email
                f"Contato: {titulo}",
                f"Nome: {nome}\nE-mail: {email}\nMensagem: {mensagem}",
                'leticia@gmail.com',  # Email de envio
                ['leticialimacgi@gmail.com'],  # Email de destino
                fail_silently=False,
            )
            return JsonResponse({'message': 'Mensagem enviada com sucesso!'})
        except Exception as e:
            return JsonResponse({'error': f"Erro ao enviar mensagem: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)
