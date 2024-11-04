***Arquivos STATIC***

**Dev: Letícia Lima**
 
**Vamos configurar nossos arquivos** *static*

```python
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

STATIC_DIR=os.path.join(BASE_DIR,'static') 

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/ 
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/' 

# STATICFILES_DIRS = [ # talvez em Produção podesse usar assim.
#     BASE_DIR / 'static',
# ]

MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/ 
# Se quiser deixar em PT BR
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

Em um ambiente de produção, é comum usar um serviço de CDN para fornecer arquivos estáticos em vez de servir diretamente do servidor Django, nesse caso, pode ser necessário configurar o **`STATICFILES_DIRS`** para incluir outros diretórios onde os arquivos estáticos estão localizados.

core/*urls.py*

```python
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG: # update 03/11/2024: (em homologa com debug true adiciona rota static)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```