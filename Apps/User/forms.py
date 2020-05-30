from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from twilio.rest import Client
from django.contrib.auth import authenticate, login



class LoginForm(AuthenticationForm):

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("Tu cuenta no ha sido verificada. Verificala para poder ingresar"),
    }

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

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data

        

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

    # Validating the username is a valid telephonic number
    def clean_username(self):
        data = self.cleaned_data['username']

        try:
            # Twilio data
            account_sid = 'AC5770f9d44bc5f3ad36f3839537c832db'
            auth_token = '02b15c643a11ed86832f973ab5780e1d'
            client = Client(account_sid, auth_token)

            # Sending SMS to user, so can activate his account
            message = client.messages.create(
                body="Tu codigo de Eats es: 123456",
                from_='+12407861324',
                to='+52'+data
                )
        except Exception as error:
            print("SMS Twilio error: {0}".format(error))
            raise forms.ValidationError('Ingresa un número telefónico válido')
        
        return data

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
        

