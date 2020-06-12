from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import crm, sms, enviarMensajes, ventas
# from .views import ProductosList, ProductosDetail, CarritoView, PagoView, PedidosView, crearPedido

urlpatterns = [
    path('', login_required(crm), name='crm'),
    path('sms', login_required(sms), name='sms'),
    path('ventas', login_required(ventas), name='ventas'),
    path('enviarMensajes', login_required(enviarMensajes), name='enviarMensajes'),
]
