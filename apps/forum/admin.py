from django.contrib import admin
from forum import models

class PostagemForumImagemInline(admin.TabularInline):
    model = models.PostagemForumImagem
    extra = 0

class PostagemForumAdmin(admin.ModelAdmin):
    inlines = [
        PostagemForumImagemInline,
    ]
    
# Register your models here.
admin.site.register(models.PostagemForum, PostagemForumAdmin)
# admin.site.register(models.PostagemForumImagem)