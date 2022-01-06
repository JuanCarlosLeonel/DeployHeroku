from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from store.models import Cliente,Produtos,Pedido,ItemPedido,EnderecoEnvio
from store.utils import cookieCart,cartData,convidadoPedido


def store(request):
    data = cartData(request)
    carrinhoItems = data['carrinhoItems']

    produtos = Produtos.objects.all()
    context = {'produtos':produtos, 'carrinhoItems':carrinhoItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    carrinhoItems = data['carrinhoItems']
    pedido = data['pedido']
    items = data['items']

    context = {'items':items, 'pedido':pedido, 'carrinhoItems':carrinhoItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    carrinhoItems = data['carrinhoItems']
    pedido = data['pedido']
    items = data['items']

    context = {'items':items, 'pedido':pedido, 'carrinhoItems':carrinhoItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produtoId']
    action = data['action']

    print('action:', action)
    print('produtoId:', produtoId)

    cliente = request.user.cliente
    produto = Produtos.objects.get(id=produtoId)
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)

    itemPedido, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)

    if action == 'add':
        itemPedido.quantidade = (itemPedido.quantidade + 1)
    elif action == 'remove':
        itemPedido.quantidade = (itemPedido.quantidade - 1)

    itemPedido.save()

    if itemPedido.quantidade <= 0:
        itemPedido.delete()

    return JsonResponse('Item foi adicionado', safe=False)


def processoPedido(request):
    transacao_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)

    else:
        cliente, pedido = convidadoPedido(request, data)

    total = data['form']['total']
    pedido.transacao_id = transacao_id
    # atencao nesse if que mudei teria que ser if total == pedido.get_cart_total
    if float(pedido.get_cart_total) != 0:
        pedido.completo = True
    pedido.save()

    if pedido.envio == True:
        EnderecoEnvio.objects.create(
            cliente=cliente,
            pedido=pedido,
            endereco=data['envio']['endereco'],
            cidade=data['envio']['cidade'],
            estado=data['envio']['estado'],
            cep=data['envio']['cep'],
        )
    
    return JsonResponse('Pagamento Completo!', safe=False)