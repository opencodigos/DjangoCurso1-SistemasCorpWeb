from django.urls import path
from perfil.views import perfil_view

urlpatterns = [
    path('<int:id>/', perfil_view, name='perfil'),
]