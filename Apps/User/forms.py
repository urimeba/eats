from django import forms
from django.forms import ModelForm
from Apps.User.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50, 
        label='Número telefónico', 
        min_length=10, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder':'Numero de teléfono', 
                'class':'form-control'
                }))
    password = forms.CharField(
        max_length=50, 
        label='Ingresa tu contraseña' , 
        min_length=5, 
        required=True, 
        widget=forms.PasswordInput(
            attrs=
            {
                'placeholder':'Contraseña', 
                'class':'form-control'
                }))

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            ]
        widgets={
            'username' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Numero de telefono'
                    }),

            'password': forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Contraseña'
                    }),

            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'correo@correo.com'
                    }),

            'first_name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'required':'True', 'placeholder':'Nombre(s)'
                    }),

            'last_name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'required':'True', 'placeholder':'Apellido(s)'
                    }),
        }


        help_texts={
            'username': 'Numero telefonico de 10 digitos, sin ladas',
            'password': 'Minimo 8 caracteres',
        }
       
