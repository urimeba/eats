from django.contrib import admin
from .models import Producto, Pedido, ProductosPedido

# class PedidoAdmin(admin.ModelAdmin):
#     readonly_fields = ('fecha',)


# Register your models here.
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ProductosPedido)
