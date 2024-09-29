
from .models import *
from django.db.models import Q
from django.views import View
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserCliente
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json
from django.core.files.storage import FileSystemStorage
import random
from django.http import JsonResponse



# Create your views here.

def home(request):
    produtos = Produto.objects.all()
    favoritos = Favorito.objects.filter(usuario=request.user).values_list('produto_id', flat=True) if request.user.is_authenticated else []
    context = {
        'produtos': produtos,
        'favoritos': list(favoritos),
    }
    return render(request, 'home.html', context)

def buscar_produto(request):
    if 'termo' in request.GET:
        termo = request.GET['termo']
        resultados = Produto.objects.filter(Q(nome_produto__icontains=termo) | Q(descricao__icontains=termo))
        if resultados:
            return render(request, 'resultado_busca.html', {'resultados': resultados, 'termo': termo})
        else:
            mensagem_alerta = f'Nenhum produto encontrado com o termo "{termo}".'
            return render(request, 'resultado_busca.html', {'mensagem_alerta': mensagem_alerta})
    else:
        return redirect('home')

def tela_cadastro(request):
    if request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        confirm_senha = request.POST['confirm_senha']
        email = request.POST['email']
        nome_completo = request.POST['nome_completo']

        # Validações de senhas
        if senha != confirm_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastro')

        # Verifica se o nome de usuário ou email já existe
        if User.objects.filter(username=nome_usuario).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return redirect('cadastro')
        if UserCliente.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('cadastro')

        # Cria o usuário padrão do Django
        usuario = User.objects.create_user(username=nome_usuario, password=senha)
        usuario.save()

        # Cria o perfil do cliente
        cliente = UserCliente(user=usuario, nome_completo=nome_completo, email=email, password=senha)
        cliente.save()

        return redirect('login')  # Redireciona para a página de login após cadastro

    return render(request, 'cadastro.html')
from django.contrib.auth import authenticate, login

def tela_login(request):
    if request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']

        # Autentica o usuário
        usuario = authenticate(request, username=nome_usuario, password=senha)

        if usuario is not None:
            login(request, usuario)  # Faz login do usuário
            return redirect('home')  # Redireciona para a página principal ou outra desejada
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')

    return render(request, 'login.html')

class ViewFoto(View):
    def get(self, request, foto_id):
        try:
            foto = Foto.objects.get(pk=foto_id)
        except Foto.DoesNotExist:
            raise Http404("Foto não existe")
        context = {'Foto' : foto}
        return render(request, 'detail.html', context)
@login_required
def favoritar(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, produto=produto).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, produto=produto)
            status = 'favoritado'
            messages.success(request, 'Produto favoritada com sucesso!')
        else:
            favorito = Favorito.objects.filter(usuario=usuario, produto=produto).first()
            favorito.delete()  # Remove o favorito se existir
            status = 'desfavoritado'
            messages.success(request, 'Produto removida dos favoritos.')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': status})
        
        return redirect('favoritos')
    
    return redirect('home')

@login_required
def lista_favoritos(request):
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user)
        return render(request, 'favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('login')
    
def detalhes_anonimo(request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        detalhes_produto = produto.detalhes()

        outros_produtos = list(Produto.objects.exclude(id=produto_id))
        random.shuffle(outros_produtos)
        outros_produtos = outros_produtos[:4]

        return render(request, 'detalhes.html', {'produto': produto, 'detalhes_produto': detalhes_produto, 'outros_produtos': outros_produtos})

