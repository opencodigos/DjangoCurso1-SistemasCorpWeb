from django.urls import path 
from config import views

urlpatterns = [
    path('', views.painel_view, name='painel'), 
]