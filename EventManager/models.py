from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

# Модель Areas
class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Модель Sponsors
class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Модель Address
class Address(models.Model):
    place_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.place_name

# Модель Types of Events
class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Модель Events
class Event(models.Model):
    name = models.CharField(max_length=255)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    place = models.ForeignKey(Address, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_date = models.DateTimeField()

    def __str__(self):
        return self.name

# Модель Event Areas
class Tickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    places = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Модель Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)

# Модель Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

# Модель Artists
class Artist(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Модель Acting Artists
class ActingArtist(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
