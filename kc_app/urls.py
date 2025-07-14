from django.urls import path
from kc_app.views import entrada_view, catalogo_view, checkout, procesar_pedido, procesar_carrito

urlpatterns = [
    path('', entrada_view, name='entrada-view'),
    path('catalogo/', catalogo_view, name='catalogo-view'),
    path('catalogo/checkout/', checkout, name='checkout'),
    path('catalogo/checkout/procesar-pedido', procesar_pedido, name='procesar-pedido'),
    path('catalogo/checkout/procesar-carrito', procesar_carrito, name='procesar-carrito'),
]