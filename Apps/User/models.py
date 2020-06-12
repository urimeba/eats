from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
import random

def random_string():
    return random.randrange(100000, 999999)

# Create your models here.
class User(AbstractUser):
    is_active = models.BooleanField(null=False, blank=False, default=False)
    email = models.EmailField(unique=True, null=True, blank=False,verbose_name='correo electronico', max_length=255)
    creditos = models.PositiveIntegerField(default=0, null=False, blank=0)
    is_cafeteria = models.BooleanField(default=False, null=False, blank=False)
    verification_code = models.PositiveIntegerField(default=random_string)

class Progreso(models.Model):
    ESTADOS = [
        ('P', 'EN PROGRESO'),
        ('L', 'LISTO'),
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
    
