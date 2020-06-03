from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Producto
import datetime 
from django.db.models import Q

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