from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('get/', views.get_messages, name='get_messages'),
    path('start/', views.start_chat, name='start_chat'),
]