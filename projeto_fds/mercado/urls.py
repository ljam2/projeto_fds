from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mercado'
urlpatterns = [
    path('', views.home, name='home'),
    path('buscar-produtos/', views.buscar_produto, name='buscar_produtos'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
    path('cadastro/', views.tela_cadastro, name='cadastro'),
    path('login/', views.tela_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('favoritar/<int:produto_id>', views.favoritar, name='favoritar'),
    path('detalhes/<int:produto_id>/', views.detalhes, name='detalhes'),
    path('detalhes/<int:produto_id>/', views.detalhes_anonimo, name='detalhes_anonimo'),
    path('carrinho/', views.exibir_carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('editar_quantidade_carrinho/<int:produto_id>/', views.editar_quantidade_carrinho, name='editar_quantidade_carrinho'),

]
