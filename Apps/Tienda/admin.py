from django.contrib import admin
from .models import Producto, Pedido, ProductosPedido

# Register your models here.
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ProductosPedido)
