from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
