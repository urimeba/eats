from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Producto, ProductosPedido, Pedido
import datetime 
from django.db.models import Q
import json

class ProductosList(ListView):
    now = datetime.datetime.now()
    actualNameDay = now.strftime('%a')

    model = Producto
    context_object_name = 'productos'
    template_name = 'store.html'
    queryset = Producto.objects.filter(
            (Q(diaSemana=actualNameDay) | Q(diaSemana='Dia')),
            unidades__gt = 0,
            is_activo = True)

class ProductosDetail(DetailView):
    model = Producto
    template_name = 'store-detail.html'

class CarritoView(TemplateView):
    template_name = 'carrito.html'

class PagoView(TemplateView):
    template_name = 'pago.html'

class PedidosView(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos_cliente.html'

    def get_queryset(self):
        queryset = Pedido.objects.filter(usuario=self.request.user)

        return queryset


def crearPedido(request):
    data = json.loads(request.body)
    pago = data['pago']
    total = data['total']
    new_pedido = Pedido(
        usuario = request.user,
        costoTotal = total,
        estado = 'AC',
        pago = pago
    )
    new_pedido.save()


    pedidos = data['pedidos']
    for pedido in pedidos:
        producto = pedidos[pedido]
        new_pedido_producto = ProductosPedido(
            producto_id = producto['id'],
            pedido = new_pedido,
        )
        new_pedido_producto.save()

    return HttpResponse('Hola')


    