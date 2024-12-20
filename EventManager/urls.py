from django.urls import path, include
import EventManager.views as v

handler403 = v.custom_permission_denied_view

urlpatterns = [
    # path('qr/<str:data>/', v.generate_qr_code, name='qr_code'),
    path('', v.EventList.as_view(), name='event_list'),
    path('events/<int:pk>', v.EventDetail.as_view(), name='event_detail'),
    path('events/create/', v.EventCreate.as_view(), name='event_create'),
    path('events/update/<int:pk>', v.EventUpdate.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', v.EventDelete.as_view(), name='event_delete'),

    path('events/<int:event_id>/buy/', v.buy_ticket, name='buy_ticket'),

    path('add-ticket/', v.add_ticket, name='add_ticket'),


    path('cart/add/<int:ticket_id>/', v.add_to_cart, name='add_to_cart'),

    path('cart/', v.cart_view, name='cart'),
    path('cart/remove/<int:cart_id>/', v.remove_from_cart, name='remove_from_cart'),

    path('cart/payment/', v.payment_page, name='payment_page'),
    path('cart/payment/process/', v.process_payment, name='process_payment'),
    path('cart/payment/qr/<int:payment_id>/', v.payment_qr_codes, name='payment_qr_codes'),

    path('history/', v.purchase_history, name='purchase_history'),
    path('history/all/', v.all_purchase_history, name='all_purchase_history'),

    path('purchase_graph/', v.generate_purchase_graph, name='purchase_graph'),


    path('register/', v.register, name='register'),

    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),


]
