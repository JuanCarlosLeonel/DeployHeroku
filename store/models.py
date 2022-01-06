from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Produtos(models.Model):
    name = models.CharField(max_length=200, null=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    imagem = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imagemURL(self):
        try:
            url = self.imagem.url
        except:
            url = ''
        return url

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False, null=True, blank=False)
    transacao_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def envio(self):
        envio = False
        pedidoitems = self.itempedido_set.all()
        for i in pedidoitems:
            if i.produto.digital == False:
                envio = True
        return envio

    @property
    def get_cart_total(self):
        pedidoitems = self.itempedido_set.all()
        total = sum([item.get_total for item in pedidoitems])
        return total

    @property
    def get_cart_items(self):
        pedidoitems = self.itempedido_set.all()
        total = sum([item.quantidade for item in pedidoitems])
        return total

class ItemPedido(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total

class EnderecoEnvio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    endereco = models.CharField(max_length=200, null=True)
    cidade = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    cep = models.CharField(max_length=200, null=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endereco