from django.shortcuts import render, HttpResponse
from Apps.User.models import User, Progreso, Nivel
from Apps.Tienda.models import Pedido, ProductosPedido, Producto
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import CharField, Value, IntegerField
import json
from twilio.rest import Client

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

    if older_pedidos>0:
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

    print(promedio_nuevas_ventas)
    print(promedio_older_ventas)

    promedio_nuevas_ventas = round(promedio_nuevas_ventas['costoTotal__avg'], 2)
    promedio_older_ventas = round(promedio_older_ventas['costoTotal__avg'], 2)
    

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
    users  = User.objects.filter(
        is_active=True,
        is_cafeteria=False
    )

    pedidos = Pedido.objects.filter(
        usuario__in=users,
    )

    # usuarios nivel plata
    plata = Progreso.objects.filter(
        estado = 'P',
        nivel__nombre='Plata',
        is_active=True,
        user__in=users
    )

    # usuarios nivel oro
    oro = Progreso.objects.filter(
        estado = 'P',
        nivel__nombre='Oro',
        is_active=True,
    )

    # usuarios sin compras
    pedidos_de_usuarios = pedidos.values('usuario')
    usuario_sin_compras = users.exclude(
        id__in=pedidos_de_usuarios
    )

    # usuarios con compras mayores a 30 dias
    today = timezone.now()
    actual_month = today.month
    last_month = today.replace(month=actual_month-1)

    pedidos_mayores = pedidos.filter(
        estado='CM',
        pago__gt=0,
        fecha__lte = last_month 
    ).values('usuario').distinct()

    usuarios_mayores = users.exclude(
        id__in = pedidos_mayores
    )

    # usuarios sin recompensas cobradas
    progresos_sin_cobrar = Progreso.objects.filter(
        user__in=users,
        estado='L',
    ).values('user')
    usuarios_sin_recompensas = users.filter(
        id__in=progresos_sin_cobrar
    )

    dic = {
        'plata':{
            'nombre':'Usuarios Plata',
            'queryset':plata, 
            'descripcion': 'Usuarios nivel Plata',
            'porcentaje': (plata.count()*100)/users.count()
            },
        'oro':{
            'nombre':'Usuarios Oro',
            'queryset':oro,
            'descripcion': 'Usuarios nivel Oro',
            'porcentaje': (oro.count()*100)/users.count()
            },
        'usuario_sin_compras':{
            'nombre':'Usuarios con 0 compras',
            'queryset':usuario_sin_compras,
            'descripcion': 'Usuarios con 0 compras',
            'porcentaje': (usuario_sin_compras.count()*100)/users.count()
            },
        'usuarios_mayores':{
            'nombre':'Usuarios sin compras en 1 mes',
            'queryset':usuarios_mayores,
            'descripcion': 'Usuarios sin compras en 1 mes',
            'porcentaje': (usuarios_mayores.count()*100)/users.count()
            },
        'usuarios_sin_recompensas':{
            'nombre':'Usuarios sin recompensas cobradas',
            'queryset':usuarios_sin_recompensas,
            'descripcion': 'Usuarios con recompensas sin cobrar',
            'porcentaje': (usuarios_sin_recompensas.count()*100)/users.count()
            },
        
    }

    return render(request, 'crm/sms.html', {'dic':dic, 'users':users})

def enviarMensajes(request):
    users  = User.objects.filter(
        is_active=True,
        is_cafeteria=False,
        is_staff=False,
        is_superuser=False
    )

    pedidos = Pedido.objects.filter(
        usuario__in=users,
    )

    # usuarios nivel plata
    plata = Progreso.objects.filter(
        estado = 'P',
        nivel__nombre='Plata',
        is_active=True,
        user__in=users
    )

    # usuarios nivel oro
    oro = Progreso.objects.filter(
        estado = 'P',
        nivel__nombre='Oro',
        is_active=True,
    )

    # usuarios sin compras
    pedidos_de_usuarios = pedidos.values('usuario')
    usuario_sin_compras = users.exclude(
        id__in=pedidos_de_usuarios
    )

    # usuarios con compras mayores a 30 dias
    today = timezone.now()
    actual_month = today.month
    last_month = today.replace(month=actual_month-1)

    pedidos_mayores = pedidos.filter(
        estado='CM',
        pago__gt=0,
        fecha__lte = last_month 
    ).values('usuario').distinct()

    usuarios_mayores = users.exclude(
        id__in = pedidos_mayores
    )

    # usuarios sin recompensas cobradas
    progresos_sin_cobrar = Progreso.objects.filter(
        user__in=users,
        estado='L',
    ).values('user')
    usuarios_sin_recompensas = users.filter(
        id__in=progresos_sin_cobrar
    )

    selected = request.POST.get('selected')
    selected = json.loads(selected)
    mensaje = request.POST.get('message')

    usuarios_mensaje = []
    
    for query in selected:
        if(query=='plata'):
            for registro in plata:
                # print(registro.user)
                usuarios_mensaje.append(registro.user)

        if(query=='oro'):
            for registro in oro:
                # print(registro.user)
                usuarios_mensaje.append(registro.user)

        if(query=='usuario_sin_compras'):
            for registro in usuario_sin_compras:
                # print(registro)
                usuarios_mensaje.append(registro)
                

        if(query=='usuarios_mayores'):
            for registro in usuarios_mayores:
                # print(registro)
                usuarios_mensaje.append(registro)

        if(query=='usuarios_sin_recompensas'):
            for registro in usuarios_sin_recompensas:
                # print(registro.user)
                usuarios_mensaje.append(registro.user)

    print(usuarios_mensaje)
    for user in usuarios_mensaje:
        try:
            account_sid = 'AC5770f9d44bc5f3ad36f3839537c832db'
            auth_token = '5da199b6e412bf237e787d83f65ca649'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=str(mensaje),
                from_='+12407861324',
                to='+52'+str(user)
                )
        except Exception as error:
            print(error)
    

    return HttpResponse('Mensajes enviados', status=200)

def ventas(request):
    pedidos = Pedido.objects.filter(
        fecha__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
    )

    promedios = pedidos.aggregate(Avg('costoTotal'), Avg('pago'))
    
    estados = pedidos.values('estado').annotate(Count('estado'))
    print(estados)

    return render(request, 'crm/ventas.html', {
        'pedidos': pedidos, 
        'promedios':promedios,
        'estados':estados
    })

def usuarios(request):
    usuarios = Progreso.objects.filter(
        is_active=True
    )
    print(usuarios)

    usuarios_nuevos = User.objects.filter(
        is_cafeteria=False,
        date_joined__gte= timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ).count()

    print(usuarios_nuevos)

    return render(request, 'crm/usuarios.html', {
        'usuarios':usuarios,
        'usuarios_nuevos':usuarios_nuevos
    })

def productos(request):
    productos = Producto.objects.filter(
        is_activo=True
    ).order_by('is_activo')
    print(productos)
    return render(request, 'crm/productos.html', {
        'productos':productos
    })

def productosPedidos(request):
    productos = ProductosPedido.objects.all()

    mas_pedidos = productos.values('producto').annotate(Count('producto')).order_by('-producto__count')
    producto_mas_vendido = Producto.objects.get(id=mas_pedidos[0]['producto'])

    calificacion_mas_vendido = productos.filter(
        producto=producto_mas_vendido
    ).aggregate(Avg('calificacion'))

    print(calificacion_mas_vendido)

    return render(request, 'crm/productospedidos.html', {
        'productos': productos,
        'mas_pedidos':mas_pedidos,
        'calificacion_mas_vendido':calificacion_mas_vendido,
        'producto_mas_vendido':producto_mas_vendido
    })

def perfil(request):
    return render(request, 'crm/profile.html')