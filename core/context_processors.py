from config.models import Logo, SEOHome

# from pages import models

def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}

def context_logo(request):
    return {'logo': Logo.objects.all().first()}

def context_seo(request):
    return {'seo': SEOHome.objects.all().first()}

def context_ga_code(request):
    return {'ga_code': GoogleAnalytics.objects.all().first()}

def context_scripts(request):
    return {
        'header_scripts': Scripts.objects.filter(place="HD", is_active=True),
        'footer_scripts': Scripts.objects.filter(place="FT", is_active=True)
        }