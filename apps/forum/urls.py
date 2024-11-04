from django.urls import path 
from forum import views

urlpatterns = [
    path('', views.lista_postagem_forum, name='lista-postagem-forum'),
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),
    path('detalhe-postagem-forum/<int:id>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
    path('editar-postagem-forum/<int:id>/', views.editar_postagem_forum, name='editar-postagem-forum'),
    path('deletar-postagem-forum/<int:id>/', views.deletar_postagem_forum, name='deletar-postagem-forum'),
    path('dashboard/lista-postagem/', views.lista_postagem_forum, name='dash-lista-postagem-forum'), 
]