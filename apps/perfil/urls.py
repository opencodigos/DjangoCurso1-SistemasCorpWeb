from django.urls import path
from perfil.views import perfil_view

urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
]