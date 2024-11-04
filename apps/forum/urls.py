from django.urls import path 
from forum import views

urlpatterns = [
    path('', views.lista_postagem_forum, name='lista-postagem-forum'),
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),
    path('detalhe-postagem-forum/<int:id>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
    path('editar-postagem-forum/<int:id>/', views.editar_postagem_forum, name='editar-postagem-forum'),
]