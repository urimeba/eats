from django import forms
from .models import User, Nivel, Progreso
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from twilio.rest import Client
import random
import os

def random_string():
    return random.randrange(100000, 999999)

class LoginForm(AuthenticationForm):

    error_messages = {
        'invalid_login': (
            "Por favor introduzca nombre de usuario y contraseña correctos. Note que puede que ambos campos sean estrictos en relación a diferencias entre mayúsculas y minúsculas."
        ),
        'inactive': ("Tu cuenta no ha sido verificada. Verificala para poder ingresar"),
    }

    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'N. telefonico'
            }))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Contraseña'
            }))

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')

    #     if username is not None and password:
    #         self.user_cache = authenticate(self.request, username=username, password=password)
    #         if self.user_cache is None:
    #             try:
    #                 user_temp = User.objects.get(username=username)
    #             except:
    #                 user_temp = None

    #             if user_temp is not None:
    #                     self.confirm_login_allowed(user_temp)
    #             else:
    #                 raise forms.ValidationError(
    #                     self.error_messages['invalid_login'],
    #                     code='invalid_login',
    #                     params={'username': self.username_field.verbose_name},
    #                 )

    #     return self.cleaned_data

class SignupForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'N. telefonico'
            })
        )
    first_name = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
            })
        )
    last_name = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
            })
        )
    email = forms.EmailField(
        required=True,
        label='',
        help_text='Será necesario para poder recuperar tu contraseña',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
            })
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

    codigo = random_string()

    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     try:
    #         # Twilio data
    #         print("-HEEEEEEEEEEEEY")
    #         print(os.environ['TWILIO_ACCOUNT_SID'])
    #         account_sid = os.environ['TWILIO_ACCOUNT_SID']
    #         auth_token = os.environ['TWILIO_AUTH_TOKEN']
    #         client = Client(account_sid, auth_token)
            

    #         # Sending SMS to user, so he can activate his account
    #         message = client.messages.create(
    #             body="Tu codigo de Eats es: {0}".format(self.codigo),
    #             from_='+12407861324',
    #             to='+52'+data
    #             )

    #         return data
    #     except Exception as error:
    #         print(error)
    #         raise forms.ValidationError('Ingresa un teléfono válido')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.verification_code = self.codigo
        if commit:
            user.save()

        nivel = Nivel.objects.get(nombre="Plata")
        progresoUsuario = Progreso(
            user=user,
            nivel=nivel,
            estado='P',
            is_active=True
        )
        progresoUsuario.save()


        return user

class VerificationForm(forms.Form):
    username = forms.CharField(
        label='Numero telefonico', 
        max_length=254, 
        required=True, 
        )
    verification_code = forms.IntegerField(
        label='Codigo de verificación',
        required=True,
        min_value=000000,
        max_value=999999
        )

    def clean(self):
        cleaned_data = super(VerificationForm, self).clean()
        username = cleaned_data['username']
        verification_code = cleaned_data['verification_code']

        try:
            user = User.objects.get(username=username, verification_code=verification_code)
            user.is_active=True
            user.save()
        except Exception as error:
            print('User with that verification code not found: {0}'.format(error))
            raise forms.ValidationError('Usuario o codigo incorrecto')

        return cleaned_data
        

