from django.shortcuts import render, HttpResponse, redirect
from .forms import  SignupForm, LoginForm, VerificationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import User, Progreso, Nivel
from Apps.Tienda.models import Pedido
from django.contrib.auth import update_session_auth_hash

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

class CustomVerification(FormView):
    template_name = 'verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('login')

    def get_success_url(self):
        messages.success(self.request, 'Cuenta verifica correctamente. Ya puedes iniciar sesión')
        return reverse('login')

class CustomProfile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(CustomProfile, self).get_context_data(**kwargs)

        
        nivel_actual = Progreso.objects.get(
            user = self.request.user,
            is_active=True,
            estado = 'P'
        )

        numero_pedidos = Pedido.objects.filter(
            usuario = self.request.user,
            estado = 'CM'
        ).count()


        context['nivel'] = nivel_actual
        context['numero_pedidos'] = numero_pedidos
        return context

def CustomResetPassword(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST, )
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña cambiada correctamente')
            return render(request, 'password.html', {
                'form': form
            })
        else:
            return render(request, 'password.html', {
                'form': form
            })
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password.html', {
            'form': form,
        })

def wrapper(request):
    if request.user.is_cafeteria:
        return redirect('crm')
    else:
        return redirect('store')
