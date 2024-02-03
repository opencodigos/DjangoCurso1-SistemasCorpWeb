from django.urls import path 
from config import views

urlpatterns = [
    path('', views.painel_view, name='painel'), 
    path('configuracao/', views.configuracao_view, name='configuracao'),  
    path('relatorio/', views.relatorio_view, name='relatorio'),
]
