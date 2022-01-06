from django.contrib import admin
from .models import Cliente,Produtos,Pedido,ItemPedido,EnderecoEnvio

admin.site.register(Cliente)
admin.site.register(Produtos)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(EnderecoEnvio)
