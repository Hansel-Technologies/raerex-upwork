from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('request/', views.service_request, name='service_request'),
    path('confirmation/', views.request_confirmation, name='request_confirmation'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('history/', views.service_history, name='service_history'),
]