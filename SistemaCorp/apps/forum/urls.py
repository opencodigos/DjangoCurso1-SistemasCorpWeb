from django.urls import path 
from forum import views

urlpatterns = [
    path('', views.lista_postagem_forum, name='lista-postagem-forum'),
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),
    path('detalhe-postagem-forum/<str:slug>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
    path('editar-postagem-forum/<str:slug>/', views.editar_postagem_forum, name='editar-postagem-forum'),
    path('deletar-postagem-forum/<str:slug>/', views.deletar_postagem_forum, name='deletar-postagem-forum'),
    path('dashboard/lista-postagem/', views.lista_postagem_forum, name='dash-lista-postagem-forum'), 

    # AJAX
    path('remover-imagem/', views.remover_imagem, name='remover-imagem'),
    
    # Comentários 
    path('adicionar-comentario/<str:slug>/', views.adicionar_comentario, name='adicionar-comentario'),
    path('editar-comentario/<int:comentario_id>/', views.editar_comentario, name='editar-comentario'),
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario, name='deletar-comentario'),
    path('responder-comentario/<int:comentario_id>/', views.responder_comentario, name='responder-comentario'),

]
