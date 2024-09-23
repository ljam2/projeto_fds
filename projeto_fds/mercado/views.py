
from .models import *
from django.views import View
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserCliente
from django.contrib.auth import authenticate, login


# Create your views here.

def home(request):
    produtos = Produto.objects.all()
    favoritos = Favorito.objects.filter(usuario=request.user).values_list('produto_id', flat=True) if request.user.is_authenticated else []
    context = {
        'produtos': produtos,
        'favoritos': list(favoritos),
    }
    return render(request, 'home.html', context)

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