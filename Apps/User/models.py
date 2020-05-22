from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    creditos = models.PositiveIntegerField(default=0, null=False, blank=0)
    is_cafeteria = models.BooleanField(default=False, null=False, blank=False)

class Progreso(models.Model):
    ESTADOS = [
        ('P', 'EN PROGRESO'),
        ('C', 'COBRADO'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=False)
    nivel = models.ForeignKey('Nivel', on_delete=models.CASCADE, null=True, blank=False)
    estado = models.CharField(max_length=1, default='P', choices=ESTADOS)
    is_active = models.BooleanField(null=False, blank=False)

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.CharField(max_length=500, null=False, blank=False)
    noComidas = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    noProductos = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    beneficios = models.CharField(max_length=500, null=False, blank=False)
    
