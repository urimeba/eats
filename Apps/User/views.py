from django.shortcuts import render, HttpResponse
from .forms import  SignupForm, LoginForm, VerificationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import User

class CustomLogin(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class CustomSignup(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def get_success_url(self):
        messages.SUCCESS(self.request, 'Usuario registrado correctamente')
        return reverse('login')

class CustomLogout(LogoutView):
    next_page = 'login'

class CustomVerification(FormView):
    template_name = 'verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('login')

    def get_success_url(self):
        messages.success(self.request, 'Cuenta verifica correctamente. Ya puedes iniciar sesión')
        return reverse('login')




