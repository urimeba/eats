from django.db import models
from Apps.User.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def nombre_imagen(instance, filename):
    return "{0}/{1}.{2}".format("productos", instance.nombre, "jpg")

# Create your models here.
class Producto(models.Model):

    DIAS = [
        ('LU', 'LUNES'),
        ('MA', 'MARTES'),
        ('MI', 'MIERCOLES'),
        ('JU', 'JUEVES'),
        ('VI', 'VIERNES'),
    ]

    nombre = models.CharField(max_length=30, null=False, blank=False, unique=True)
    descripcion = models.CharField(max_length=50, null=False, blank=False)
    costo = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    unidades = models.PositiveIntegerField()
    is_preparado = models.BooleanField()
    is_activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to=nombre_imagen, max_length=100)
    diaSemana = models.CharField(max_length=2, null=True, blank=True, choices=DIAS)

class ProductosPedido(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Pedido(models.Model):
    ESTADOS = [
        ('AC', 'Activo'),
        ('CO', 'Confirmado'),
        ('CA', 'Cancelado'),
        ('CM', 'Completado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    costoTotal = models.DecimalField(max_digits=4, decimal_places=2)
    estado = models.CharField(max_length=2, choices=ESTADOS, null=False, blank=False, )
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    # cancelado = 3 minutos

