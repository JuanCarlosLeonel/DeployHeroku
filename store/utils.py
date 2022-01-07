import json
from store.models import Cliente,Produtos,Pedido,ItemPedido,EnderecoEnvio


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    pedido = {'get_cart_total':0, 'get_cart_items':0, 'envio':False}
    carrinhoItems = pedido['get_cart_items']

    for i in cart:
        try:
            carrinhoItems += cart[i]["quantidade"]

            produto = Produtos.objects.get(id=i)
            total = (produto.preco * cart[i]["quantidade"])

            pedido['get_cart_total'] += total
            pedido['get_cart_items'] += cart[i]["quantidade"]

            item = {
                'produto':{
                    'id':produto.id,
                    'name':produto.name,
                    'preco':produto.preco,
                    'imagemURL':produto.imagemURL,
                    },
                'quantidade':cart[i]["quantidade"],
                'get_total':total
            }
            items.append(item)

            if produto.digital == False:
                pedido['envio'] = True
        except:
            pass
    return {'carrinhoItems':carrinhoItems, 'pedido':pedido, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        items = pedido.itempedido_set.all()
        carrinhoItems = pedido.get_cart_items
    else:
        cookieData = cookieCart(request)
        carrinhoItems = cookieData['carrinhoItems']
        pedido = cookieData['pedido']
        items = cookieData['items']
    return {'carrinhoItems':carrinhoItems, 'pedido':pedido, 'items':items}


def convidadoPedido(request, data):
    print('Usuário não esta logado')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    password = data['form']['password']

    cookieData = cookieCart(request)
    items = cookieData['items']

    cliente, created = Cliente.objects.get_or_create(
        email=email,
        )
    cliente.password = password
    cliente.name = name
    cliente.save()

    pedido = Pedido.objects.create(
        cliente=cliente,
        completo=False,
        )

    for item in items:
        produto = Produtos.objects.get(id=item['produto']['id'])

        itemPedido = ItemPedido.objects.create(
            produto=produto,
            pedido=pedido,
            quantidade=item['quantidade']
        )
    return cliente, pedido