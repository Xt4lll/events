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

    path('register/', v.register, name='register'),

    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),


]
