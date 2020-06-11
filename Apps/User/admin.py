from django.contrib import admin
from .models import User, Nivel, Progreso
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Extra', {
            'fields': (
                'is_cafeteria',
                'creditos',
                'verification_code',
            )
        }),
    )

admin.site.register(User, UsuarioAdmin)
admin.site.register(Nivel)
admin.site.register(Progreso)