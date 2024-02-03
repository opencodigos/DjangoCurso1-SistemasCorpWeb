from django.urls import path 
from pages import views 

urlpatterns = [
    path('', views.paginas_view, name='home'), 
    path('sobre/', views.paginas_view, name='sobre'), 
    path('faq/', views.paginas_view, name='faq'), 
    path('contato/', views.paginas_view, name='contato'), 
]