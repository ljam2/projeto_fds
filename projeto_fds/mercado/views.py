
from .models import *
from django.db.models import Q
from django.views import View
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.core.files.storage import FileSystemStorage
import random
from django.http import JsonResponse
from django.contrib import messages
from .models import UserCliente



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
            return render(request, 'resultado_busca.html', {'mensagem_alerta': mensagem_alerta, 'termo': termo})
    else:
        return redirect('mercado:home')

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
            return redirect('mercado:cadastro')

        # Verifica se o nome de usuário ou email já existe
        if User.objects.filter(username=nome_usuario).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return redirect('mercado:cadastro')
        if UserCliente.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('mercado:cadastro')

        # Cria o usuário padrão do Django
        usuario = User.objects.create_user(username=nome_usuario, password=senha)
        usuario.save()

        # Cria o perfil do cliente
        cliente = UserCliente(user=usuario, nome_completo=nome_completo, email=email, password=senha)
        cliente.save()

        return redirect('mercado:login')  # Redireciona para a página de login após cadastro

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

            # Verifica se o usuário é um fornecedor
            if hasattr(usuario, 'usercliente') and usuario.usercliente.is_supplier:
                return redirect('mercado:fornecedor_home')  # Redireciona para a home do fornecedor
            else:
                return redirect('mercado:home')  # Redireciona para a home padrão

        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    request.session.flush()
    return redirect('mercado:home')

class ViewFoto(View):
    def get(self, request, foto_id):
        try:
            foto = Foto.objects.get(pk=foto_id)
        except Foto.DoesNotExist:
            raise Http404("Foto não existe")
        context = {'Foto' : foto}
        return render(request, 'detalhe_foto.html', context)
    
@login_required
def favoritar(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, produto=produto).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, produto=produto)
            status = 'favoritado'
        else:
            favorito = Favorito.objects.filter(usuario=usuario, produto=produto).first()
            favorito.delete()
            status = 'desfavoritado'
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': status})
        
        return redirect('mercado:favoritos')
    
    return redirect('mercado:home')

@login_required
def lista_favoritos(request):
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user)
        return render(request, 'favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('mercado:login')
    
def detalhes_anonimo(request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        detalhes_produto = produto.detalhes()

        outros_produtos = list(Produto.objects.exclude(id=produto_id))
        random.shuffle(outros_produtos)
        outros_produtos = outros_produtos[:4]

        return render(request, 'detalhes.html', {'produto': produto, 'detalhes_produto': detalhes_produto, 'outros_produtos': outros_produtos})

@login_required
def detalhes(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    usuario = request.user
    favorito = Favorito.objects.filter(usuario=usuario, produto=produto).exists()
    detalhes_produto = produto.detalhes()

    outros_produto = list(Produto.objects.exclude(id=produto_id))
    random.shuffle(outros_produto)
    outros_produto = outros_produto[:4]


    today = timezone.localdate()

    visita_hoje = Historico.objects.filter(
        usuario=usuario, 
        produto=produto, 
        visited_at__date=today,
    ).exists()

    if not visita_hoje:
        Historico.objects.create(usuario=usuario, produto=produto, visited_at=timezone.now())


    return render(request, 'detalhes.html', {
        'produto': produto,
        'detalhes_produto': detalhes_produto,
        'favorito': favorito,
        'outros_produto': outros_produto,
    })
@login_required
def exibir_carrinho(request):
    usuario = request.user

    # Obtém o carrinho do usuário (caso exista)
    carrinho = Carrinho.objects.filter(usuario=usuario).first()

    # Obtém os itens do carrinho, se existir um carrinho ativo
    itens = Item_Carrinho.objects.filter(carrinho=carrinho) if carrinho else []

    # Calcula o total do carrinho
    total = sum(item.produto.preco * item.quantidade for item in itens)

    # Renderiza o template do carrinho, passando os itens e o total
    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total,
    })
@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    usuario = request.user

    # Verifica se o usuário já tem um carrinho ativo
    carrinho, created = Carrinho.objects.get_or_create(usuario=usuario)

    # Verifica se o produto já está no carrinho
    item_carrinho, item_created = Item_Carrinho.objects.get_or_create(carrinho=carrinho, produto=produto)

    if not item_created:
        # Se o item já existe, aumenta a quantidade
        item_carrinho.quantidade += 1
        item_carrinho.save()
    else:
        # Define a quantidade inicial como 1
        item_carrinho.quantidade = 1
        item_carrinho.save()

    messages.success(request, 'Produto adicionado ao carrinho com sucesso!')
    return redirect('mercado:detalhes_anonimo', produto_id=produto.id)
@login_required
def remover_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    usuario = request.user

    # Encontra o carrinho do usuário
    carrinho = get_object_or_404(Carrinho, usuario=usuario)

    # Verifica se o produto está no carrinho e remove
    item_carrinho = Item_Carrinho.objects.filter(carrinho=carrinho, produto=produto).first()

    if item_carrinho:
        if item_carrinho.quantidade > 1:
            # Se a quantidade for maior que 1, diminui
            item_carrinho.quantidade -= 1
            item_carrinho.save()
        else:
            # Caso contrário, remove o item do carrinho
            item_carrinho.delete()
        messages.success(request, 'Produto removido do carrinho com sucesso!')
    else:
        messages.error(request, 'Produto não encontrado no carrinho.')

    return redirect('mercado:detalhes', produto_id=produto.id)
@login_required
def editar_quantidade_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    usuario = request.user
    nova_quantidade = int(request.POST.get('quantidade', 1))

    if nova_quantidade < 1:
        messages.error(request, 'A quantidade deve ser maior que zero.')
        return redirect('mercado:detalhes', produto_id=produto.id)

    # Encontra o carrinho do usuário
    carrinho = get_object_or_404(Carrinho, usuario=usuario)

    # Verifica se o produto está no carrinho e edita a quantidade
    item_carrinho = Item_Carrinho.objects.filter(carrinho=carrinho, produto=produto).first()

    if item_carrinho:
        item_carrinho.quantidade = nova_quantidade
        item_carrinho.save()
        messages.success(request, 'Quantidade atualizada com sucesso!')
    else:
        messages.error(request, 'Produto não encontrado no carrinho.')

    return redirect('mercado:detalhes', produto_id=produto.id)

def fornecedor_check(user):
    return user.usercliente.is_supplier
@login_required
@user_passes_test(fornecedor_check)
def cadastrar_produto(request):
    if request.method == 'POST':
        nome_produto = request.POST.get('nome_produto')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')
        disponivel = request.POST.get('disponivel') == 'on'

        if not nome_produto or not descricao or not preco or not estoque:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('mercado:cadastrar_produto')

        produto = Produto(
            nome_produto=nome_produto,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            disponivel=disponivel,
            fornecedor=request.user  
        )
        produto.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect('mercado:home')
    
    return render(request, 'cadastrar_produto.html')
def historico_vendas(request):
    produtos_do_vendedor = Produto.objects.filter(fornecedor=request.user)
    vendas = Venda.objects.filter(produto__in=produtos_do_vendedor)

    context = {
        'vendas': vendas,
    }
    return render(request, 'historico_vendas.html', context)