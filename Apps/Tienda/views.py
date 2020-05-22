from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

class Store(View):
    def get(self, request):
        return render(request, 'store.html')
