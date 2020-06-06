from django.urls import path
from .views import ProductosList, ProductosDetail, CarritoView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(ProductosList.as_view()), name='store'),
    path('<int:pk>', login_required(ProductosDetail.as_view()), name='store-detail'),
    path('carrito', login_required(CarritoView.as_view()), name='carrito'),
]
