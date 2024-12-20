from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Пользовательская модель User
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Роль')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Модель Areas
class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'


# Модель Sponsors
class Sponsor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'


# Модель Address
class Address(models.Model):
    place_name = models.CharField(max_length=255, verbose_name='Название места')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return self.place_name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


# Модель Types of Events
class EventType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'


# Модель Artists
class Artist(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    description = models.CharField(max_length=255, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'


# Модель Events
class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, verbose_name='Спонсор')
    place = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Место')
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='Тип мероприятия')
    event_date = models.DateTimeField(verbose_name='Дата и время')
    artists = models.ManyToManyField(Artist, related_name='events', verbose_name='Артисты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


# Модель Tickets
class Tickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Зона')
    places = models.IntegerField(verbose_name='Места')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.event.name} - {self.area}'

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


# Модель Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, verbose_name='Билет')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


# Модель Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=255, verbose_name='Статус')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', null=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    card_number = models.CharField(max_length=16, verbose_name='Номер карты')
    event_info = models.TextField(verbose_name='Информация о мероприятиях')
    purchase_date = models.DateTimeField(default=now, verbose_name='Дата покупки')

    def __str__(self):
        return f"Оплата #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
