from django.db import models
from Apps.User.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

def nombre_imagen(instance, filename):
    return "{0}/{1}.{2}".format("productos", instance.nombre, "jpg")

# Create your models here.
class Producto(models.Model):

    DIAS = [
        ('Mon', 'Lunes'),
        ('Tue', 'Martes'),
        ('Wed', 'Miercoles'),
        ('Thu', 'Jueves'),
        ('Fri', 'Viernes'),
        ('Dia', 'Diario'),
    ]

    descripcion = models.CharField(max_length=500, null=False, blank=False)
    nombre = models.CharField(max_length=30, null=False, blank=False, unique=True)
    costo = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    unidades = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    is_preparado = models.BooleanField()
    is_activo = models.BooleanField(default=True)
    imagen = models.CharField(max_length=500, null=False, blank=False)
    diaSemana = models.CharField(max_length=3, null=True, blank=True, choices=DIAS)

    def __str__(self):
        return self.nombre

class ProductosPedido(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField(null=True, blank=True, default=1,
    validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return "{0} en {1}".format(
            self.producto.nombre,
            self.pedido
        )

class Pedido(models.Model):
    ESTADOS = [
        ('AC', 'Activo'),
        ('CO', 'Confirmado'),
        ('CA', 'Cancelado'),
        ('CM', 'Completado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    costoTotal = models.DecimalField(max_digits=5, decimal_places=2)
    estado = models.CharField(max_length=2, choices=ESTADOS, null=False, blank=False, )
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    pago = models.DecimalField(max_digits=5, decimal_places=2, default=01.00)

    def __str__(self):
        return "Pedido #{0} por {1} el {2}".format(
            self.id, 
            self.usuario.username, 
            self.fecha
        )

