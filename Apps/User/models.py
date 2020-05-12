from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # telefono = models.CharField(max_length= 13, unique=True, null=False, blank=False)
    creditos = models.PositiveIntegerField(default=0, null=False, blank=0)
    nivel = models.ForeignKey('Niveles', on_delete=models.CASCADE)
    is_cafeteria = models.BooleanField(default=False, null=False, blank=False)

class Niveles(models.Model):
    ESTADOS = [
        ('P', 'EN PROGRESO'),
        ('C', 'COBRADO'),
    ]

    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.CharField(max_length=500, null=False, blank=False)
    noComidas = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    noProductos = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    beneficios = models.CharField(max_length=500, null=False, blank=False)
    estado = models.CharField(max_length=1, default='P', choices=ESTADOS)
