from django.contrib import admin
from .models import User, Nivel
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Extra', {
            'fields': (
                'is_cafeteria',
                'nivel',
                'creditos'
            )
        }),
    )

admin.site.register(User, UsuarioAdmin)
admin.site.register(Nivel)