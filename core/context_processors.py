from config.models import Logo, SEOHome

# from pages import models

def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}

def context_logo(request):
    return {'logo': Logo.objects.all().first()}

def context_seo(request):
    return {'seo': SEOHome.objects.all().first()}

