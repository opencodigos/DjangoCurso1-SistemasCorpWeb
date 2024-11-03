from django.urls import path, include
from contas import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),  # Django auth
	path('desconectado-inatividade/',  views.timeout_view, name='timeout'), 
 	path('sair/', views.logout_view, name='logout'),
 	path('entrar/', views.login_view, name='login'), 
  	path('criar-conta/', views.register_view, name='register'),
]