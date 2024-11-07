from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
import qrcode
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# def generate_qr_code(request, data):
#     # Создание объекта QR-кода
#     qr = qrcode.QRCode(
#         version=1,  # Размер QR-кода
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,  # Размер каждого квадрата
#         border=4,  # Толщина границы
#     )
#
#     # Добавление данных (например, строки)
#     qr.add_data(data)
#     qr.make(fit=True)
#
#     # Создание изображения QR-кода
#     img = qr.make_image(fill='black', back_color='white')
#
#     # Сохранение изображения в поток байтов
#     buffer = BytesIO()
#     img.save(buffer)
#     buffer.seek(0)
#
#     # Возвращаем изображение как HTTP-ответ
#     return HttpResponse(buffer, content_type="image/png")

def custom_permission_denied_view(request, exception=None):
    return render(request, 'EventManager/exceptions/403.html', status=403)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'EventManager/registration/login.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('event_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('event_list')
    else:
        form = AuthenticationForm()
    return render(request, 'EventManager/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('register')

class EventList(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'EventManager/Events.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return self.model.objects.all()

class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'EventManager/EventDetail.html'
    context_object_name = 'event'