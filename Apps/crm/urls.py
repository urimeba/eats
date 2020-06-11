from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import crm, sms
# from .views import ProductosList, ProductosDetail, CarritoView, PagoView, PedidosView, crearPedido

urlpatterns = [
    path('', login_required(crm), name='crm'),
    path('sms', login_required(sms), name='sms'),
]
