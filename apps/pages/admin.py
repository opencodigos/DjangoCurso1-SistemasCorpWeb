from django.contrib import admin
from pages import models

# Register your models here.
admin.site.register(models.Pagina)
admin.site.register(models.TipoBloco)
admin.site.register(models.Conteudo)
admin.site.register(models.Blocos)