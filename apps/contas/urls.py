from django.urls import path 
from contas import views

urlpatterns = [
	path('desconectado-inatividade/',  views.timeout_view, name='timeout'), 
]