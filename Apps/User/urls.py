from django.contrib import admin
from django.urls import path
from Apps.User import views as views_user
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views_user.CustomLogin.as_view(), name="login"),
    path('registro', views_user.CustomSignup.as_view(), name="signup"),
    path('verificar', views_user.CustomVerification.as_view(), name="verification"),
    path('logout', login_required(views_user.CustomLogout.as_view()), name="logout"),
    
]
