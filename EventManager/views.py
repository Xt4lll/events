from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
import qrcode
from django.http import HttpResponse
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin


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

class AdminOrManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['admin', 'manager']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

def custom_permission_denied_view(request, exception=None):
    return render(request, 'EventManager/exceptions/../templates/403.html', status=403)

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
    return render(request, 'EventManager/registration/login.html', {'form': form, 'title':'Регистрация'})


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в систему.")
        return redirect('event_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
    else:
        form = AuthenticationForm()

    return render(request, 'EventManager/registration/login.html', {'form': form, 'title':'Авторизация'})

def logout_view(request):
    logout(request)
    return redirect('login')


# Event Views

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

class EventCreate(LoginRequiredMixin, AdminOrManagerRequiredMixin, CreateView):
    model = Event
    template_name = 'EventManager/EventEditCreate.html'
    form_class = EventForm
    context_object_name = 'event'

    success_url = reverse_lazy('event_list')

class EventUpdate(LoginRequiredMixin, AdminOrManagerRequiredMixin, UpdateView):
    model = Event
    template_name = 'EventManager/EventEditCreate.html'
    form_class = EventForm
    context_object_name = 'event'

    success_url = reverse_lazy('event_list')

class EventDelete(LoginRequiredMixin, AdminOrManagerRequiredMixin, DeleteView):
    model = Event
    # template_name = 'EventManager/EventDetail.html'
    context_object_name = 'event'
    success_url = reverse_lazy('event_list')


# Buy Ticket

@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Tickets.objects.filter(event=event)

    return render(request, 'EventManager/BuyTicket.html', {
        'event': event,
        'tickets': tickets,
    })

@login_required
def add_to_cart(request, ticket_id):
    ticket = get_object_or_404(Tickets, id=ticket_id)
    event_id = ticket.event.id
    if ticket.places > 0:
        Cart.objects.create(user=request.user, ticket=ticket)
        ticket.places -= 1
        ticket.save()
        messages.success(request, "Билет добавлен в корзину!")
    else:
        messages.error(request, "Билетов больше нет.")
    return redirect('buy_ticket', event_id=ticket.event.id)


# Cart views

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('ticket__event', 'ticket__area')
    return render(request, 'EventManager/Cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    ticket = cart_item.ticket
    cart_item.delete()

    ticket.places += 1
    ticket.save()

    messages.success(request, "Билет удалён из корзины.")
    return redirect('cart')


# Payment views

@login_required
def payment_page(request):
    return render(request, 'EventManager/Payment.html')


@login_required
def process_payment(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        card_number = request.POST.get('card_number')

        # Получаем корзину пользователя
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Ваша корзина пуста!")
            return redirect('cart')

        # Собираем информацию о мероприятиях
        event_info = "\n".join([
            f"{item.ticket.event.name} - {item.ticket.area.name}, Цена: {item.ticket.price} ₽"
            for item in cart_items
        ])

        # Сохраняем данные в базу
        payment = Payment.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            card_number=card_number[-4:],  # Храним только последние 4 цифры
            event_info=event_info
        )

        # Очищаем корзину пользователя
        cart_items.delete()

        messages.success(request, "Оплата успешно завершена!")
        return redirect('payment_qr_codes', payment_id=payment.id)

    return redirect('payment_page')


@login_required
def payment_qr_codes(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"Имя: {payment.first_name} {payment.last_name}\n"
    qr_data += f"Номер карты: **** **** **** {payment.card_number}\n"
    qr_data += f"Мероприятия:\n{payment.event_info}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Создание изображения QR-кода
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Возвращаем изображение на страницу
    return HttpResponse(buffer, content_type="image/png")


# History views

@login_required
def purchase_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'EventManager/PurchaseHistory.html', {'payments': payments})

@login_required
@user_passes_test(lambda user: user.role in ['manager', 'admin'], login_url='/403/')
def all_purchase_history(request):
    payments = Payment.objects.all().order_by('-purchase_date')
    return render(request, 'EventManager/AllPurchaseHistory.html', {'payments': payments})
