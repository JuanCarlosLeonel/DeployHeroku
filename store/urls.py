from django.urls import path
from store.views import cart,checkout,store,updateItem,processoPedido

urlpatterns = [
    path('', store, name="store"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),

    path('update_item/', updateItem, name="update_item"),
    path('processo_pedido/', processoPedido, name="processo_pedido"),
]