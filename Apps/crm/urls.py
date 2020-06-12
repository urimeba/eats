from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import crm, sms, enviarMensajes, ventas, usuarios, productos, productosPedidos, perfil
# from .views import ProductosList, ProductosDetail, CarritoView, PagoView, PedidosView, crearPedido

urlpatterns = [
    path('', login_required(crm), name='crm'),
    path('sms', login_required(sms), name='sms'),
    path('ventas', login_required(ventas), name='ventas'),
    path('usuarios', login_required(usuarios), name='usuarios'),
    path('productos', login_required(productos), name='productos'),
    path('productospedidos', login_required(productosPedidos), name='productospedidos'),
    path('perfil', login_required(perfil), name='perfil'),
    path('enviarMensajes', login_required(enviarMensajes), name='enviarMensajes'),
]
