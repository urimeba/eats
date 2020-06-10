from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ProductosList, ProductosDetail, CarritoView, PagoView, PedidosView, crearPedido

urlpatterns = [
    path('', login_required(ProductosList.as_view()), name='store'),
    path('<int:pk>', login_required(ProductosDetail.as_view()), name='store-detail'),
    path('carrito', login_required(CarritoView.as_view()), name='carrito'),
    path('pago', login_required(PagoView.as_view()), name='pago'),
    path('pedidos', login_required(PedidosView.as_view()), name='pedidos_cliente'),
    path('crearPedido', crearPedido, name='crearPedido')
]
