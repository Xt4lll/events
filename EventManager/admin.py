from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'role')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'place_name', 'address')

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sponsor', 'place', 'type', 'event_date')

@admin.register(Tickets)
class EventAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'area', 'places', 'price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'card_number', 'event_info', 'purchase_date')

# @admin.register(ActingArtist)
# class ActingArtistAdmin(admin.ModelAdmin):
#     list_display = ('id', 'artist', 'event')