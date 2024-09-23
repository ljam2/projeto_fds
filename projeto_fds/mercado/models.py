from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg
from datetime import datetime

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
    
class Produto(models.Model):
    nome_produto = models.CharField(max_length=50, null=True)
    descricao = models.TextField(blank=False, default='')

    def __str__(self):
        return self.nome_produto

class Foto(models.Model):
    produto = models.ForeignKey(Produto, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos_produto/', blank=True, null=True)

    def __str__(self):
        return f"Foto para {self.produto.nome_produto}"
