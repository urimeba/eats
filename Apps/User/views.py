from django.shortcuts import render
from .forms import LoginForm, RegisterForm

# Create your views here.
def loginn(request):
    form = LoginForm()
    return render(request, 'login.html', {
        'form':form
    })

def register(request):
    form = RegisterForm()
    return render(request, 'register.html', {
        'form':form
    })