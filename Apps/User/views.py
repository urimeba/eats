from django.shortcuts import render
from .forms import  SignupForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse


class CustomLogin(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class CustomSignup(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Usuario registrado correctamente')
        return reverse('login')

class CustomLogout(LogoutView):
    next_page = 'login'