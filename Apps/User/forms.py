from django import forms
from django.forms import ModelForm
from Apps.User.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Numero telefónico', 
        widget=forms.TextInput(attrs={
            'class': 'aqui_pon_tus_clases',
            'placeholder': '10 digitos, sin lada'
            }))
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'aqui_pon_tus_clases',
            'placeholder':'Contraseña'
            }))

class SignupForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Número telefónico',
        )
    first_name = forms.CharField(
        required=True,
        label='Nombre(s)'
        )
    last_name = forms.CharField(
        required=True,
        label='Apellido(s)'
        )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        help_text='Será necesario para poder recuperar tu contraseña'
        )

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2',
            ]