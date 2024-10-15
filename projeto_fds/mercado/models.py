from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg
from datetime import datetime
from .models import *
from .models import Produto


class UserCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome_completo = models.CharField(max_length=150, default="Desconhecido")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True)
    confirm_password = models.CharField(max_length=255, null=True)
    is_supplier = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)

    def __str__(self):
        return self.email
    
from django.db import models
class Carrinho(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    adicionado=models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return f"carrinho {self.id}"
    def total(self):
        return sum(item.subtotal() for item in self.itens.all())
class Produto(models.Model):
    nome_produto = models.CharField(max_length=50, null=True)
    descricao = models.TextField(blank=False, default='')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    estoque = models.IntegerField(default=0)
    data_adicionado = models.DateTimeField(default=timezone.now)
    disponivel = models.BooleanField(default=True)


    def __str__(self):
        return self.nome_produto
    
    def detalhes(self):
        return (
            f"nome: {self.nome_produto}\n"
            f"descrição: {self.descricao}\n"
            f"preço: R$ {self.preco:.2f}\n"
            f"estoque: {self.estoque} unidades\n"
            f"data: {self.data_adicionado.strftime('%d/%m/%Y %H:%M')}\n"
            f"disponível: {'Sim' if self.disponivel else 'Não'}"
        )
    def get_short_description(self):
        if len(self.descricao) > 70:
            return self.descricao[:70].__add__("...")
        else:
            return self.descricao


class Foto(models.Model):
    produto = models.ForeignKey(Produto, related_name='fotos_produto', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos_produto/', blank=True, null=True)

    def __str__(self):
        return f"Foto for {self.produto.nome_produto}"
class Item_Carrinho(models.Model):
    carrinho=models.ForeignKey(Carrinho,related_name="itens", on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade=models.PositiveIntegerField(default=1)
    def subtotal(self):
       return self.produto.preco*self.quantidade
    def _str_(self):
        return f"{self.quantidade} x {self.produto.nome_produto}"

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome_produto}'
    
class Historico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'produto', 'visited_at')

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome_produto}'
 
class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="vendas")
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compras")
    quantidade = models.PositiveIntegerField()
    data_venda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda de {self.produto.nome_produto} para {self.comprador.username} em {self.data_venda}"


