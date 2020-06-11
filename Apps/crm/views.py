from django.shortcuts import render
from Apps.User.models import User
from Apps.Tienda.models import Pedido, ProductosPedido
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import datetime

# Create your views here.
def crm(request):

    # FORMULACION DE PORCENTAJE Y CUENTA DE NUEVOS Y VIEJOS USUARIOS
    new_users = User.objects.filter(
        date_joined__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ).count()

    older_users = User.objects.filter(
        date_joined__gte=timezone.now().replace(month=datetime.now().month-1, day=1, hour=0, minute=0, second=0, microsecond=0),
        date_joined__lte=timezone.now().replace( day=1, hour=0, minute=0, second=0, microsecond=0),
    ).count()

    porcentaje_usuarios = (new_users * 100) / older_users

    # FORMULACION DE PORCENTAJE DE VENTAS
    nuevos_pedidos = Pedido.objects.filter(
        fecha__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        estado = 'CM'
    ).count()

    older_pedidos = Pedido.objects.filter(
        fecha__gte=timezone.now().replace(month=datetime.now().month-1, day=1, hour=0, minute=0, second=0, microsecond=0),
        fecha__lte=timezone.now().replace( day=1, hour=0, minute=0, second=0, microsecond=0),
        estado = 'CM'
    ).count()

    porcentaje_ventas = (nuevos_pedidos * 100) / older_pedidos

    # FORMULACION DE PORCENTAJE DE COSTOS
    promedio_nuevas_ventas = Pedido.objects.filter(
        fecha__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        estado = 'CM'
    ).values('id').aggregate(Avg('costoTotal'))

    promedio_older_ventas = Pedido.objects.filter(
        fecha__gte=timezone.now().replace(month=datetime.now().month-1, day=1, hour=0, minute=0, second=0, microsecond=0),
        fecha__lte=timezone.now().replace( day=1, hour=0, minute=0, second=0, microsecond=0),
        estado = 'CM'
    ).values('id').aggregate(Avg('costoTotal'))

    promedio_nuevas_ventas = round(promedio_nuevas_ventas['costoTotal__avg'], 2)
    promedio_older_ventas = round(promedio_older_ventas['costoTotal__avg'], 2)
    print(promedio_nuevas_ventas)
    print(promedio_older_ventas)

    porcentaje_promedio_ventas = (promedio_nuevas_ventas * 100) / promedio_older_ventas
    porcentaje_promedio_ventas = round(porcentaje_promedio_ventas, 2)


    return render(request, 'crm/dashboard.html', {
        'new_users':new_users,
        'porcentaje_usuarios':porcentaje_usuarios,
        'nuevos_pedidos':nuevos_pedidos,
        'porcentaje_ventas':porcentaje_ventas,
        'promedio_nuevas_ventas':promedio_nuevas_ventas,
        'porcentaje_promedio_ventas':porcentaje_promedio_ventas,
        'var':25
    })

def sms(request):
    return render(request, 'crm/sms.html')

