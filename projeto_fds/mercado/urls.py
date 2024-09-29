# mercado/urls.py
from django.urls import path
from . import views

app_name = 'mercado'
urlpatterns = [
    path('', views.home, name='home'),
    path('buscar-produtos/', views.buscar_produto, name='buscar_produtos'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
    path('cadastro/', views.tela_cadastro, name='cadastro'),
    path('login/', views.tela_login, name='login'),
    path('favoritar/<int:produto_id>', views.favoritar, name='favoritar'),
    

]