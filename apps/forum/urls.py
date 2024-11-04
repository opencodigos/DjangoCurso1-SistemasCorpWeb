from django.urls import path 
from forum import views

urlpatterns = [
    path('', views.lista_postagem_forum, name='lista-postagem-forum'),
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),

]