from django.contrib import admin
from .models import *

# Função para registrar um modelo se não estiver registrado
def register_model(admin_site, model):
    if model not in admin_site._registry:
        admin_site.register(model)
    else:
        print(f"O modelo {model.__name__} já está registrado.")
        
# Register your models here.
register_model(admin.site, Produto)
register_model(admin.site, Foto)
register_model(admin.site, Carrinho)
register_model(admin.site, UserCliente)
register_model(admin.site, Item_Carrinho)
register_model(admin.site, Favorito)
register_model(admin.site, Historico)
register_model(admin.site, Venda)
register_model(admin.site, Compra)