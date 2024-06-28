from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages

from FlyWheelMedicalApp.forms import ClientRegistrationForm
from FlyWheelMedicalApp.models import Client, Manager, Doctor


class LoginView(View):
    def get(self, request):
        return render(request, 'auntification/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            clients = Client.objects.all()
            managers = Manager.objects.all()
            doctors = Doctor.objects.all()

            for client in clients:
                if client.user == user:
                    return HttpResponseRedirect(reverse('client_dashboard'))

            for manager in managers:
                if manager.user == user:
                    return HttpResponseRedirect(reverse('admin:index'))

            for doctor in doctors:
                if doctor.user == user:
                    return HttpResponseRedirect(reverse('doctor_dashboard'))
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
            return render(request, 'auntification/login.html')


class RegistrationView(View):
    def get(self, request):
        form = ClientRegistrationForm()
        return render(request, 'auntification/registration.html', {'form': form})

    def post(self, request):
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            # Проверка на уникальность имени пользователя
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                # Если имя пользователя уже существует, выводим сообщение об ошибке
                form.add_error('username', 'Имя пользователя занято.')
                return render(request, 'auntification/registration.html', {'form': form})

            # Создание пользователя и клиента
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password']
            )
            client = Client.objects.create(
                user=user,
                FirstName=form.cleaned_data['FirstName'],
                LastName=form.cleaned_data['LastName'],
                Surname=form.cleaned_data['Surname'],
                ContactNumber=form.cleaned_data['ContactNumber']
            )
            return redirect('login')  # Перенаправьте пользователя на страницу после регистрации
        return render(request, 'auntification/registration.html', {'form': form})


