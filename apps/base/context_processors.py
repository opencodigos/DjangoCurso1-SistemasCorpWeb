from config.models import Logo, SEOHome, GoogleAnalytics, Scripts

def context_social(request):
    return {
        'social': 'Exibir este contexto em qualquer lugar!'
        }
 
def get_logo(request):
    return {
        'logo': Logo.objects.all().first()
    }
    
def get_seo(request):
    return {
        'seo': SEOHome.objects.first()
    }
    
def get_ga_code(request):
    return {
        'ga_code': GoogleAnalytics.objects.first()
    }
    
def get_scripts(request):
    return {
        'header_scripts': Scripts.objects.filter(place='HD', is_active=True),
        'footer_scripts': Scripts.objects.filter(place='FT', is_active=True),
    }