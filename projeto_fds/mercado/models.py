from django.db import models

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
