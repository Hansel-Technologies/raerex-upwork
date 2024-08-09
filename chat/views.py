from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage, ChatSession
from django.http import JsonResponse
import json

def chat_view(request):
    return render(request, 'chat/chat.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        
        if request.user.is_authenticated:
            chat_session, created = ChatSession.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_id = request.session.get('chat_session_id')
            if not session_id:
                guest_name = data.get('guest_name')
                guest_email = data.get('guest_email')
                if not guest_name or not guest_email:
                    return JsonResponse({'status': 'error', 'message': 'Name and email are required'})
                chat_session = ChatSession.objects.create(guest_name=guest_name, guest_email=guest_email)
                request.session['chat_session_id'] = chat_session.id
            else:
                chat_session = ChatSession.objects.get(id=session_id)

        if message:
            chat_message = ChatMessage.objects.create(session=chat_session, message=message)
            return JsonResponse({'status': 'success', 'message': chat_message.message})
    return JsonResponse({'status': 'error'})

def get_messages(request):
    if request.user.is_authenticated:
        chat_session, created = ChatSession.objects.get_or_create(user=request.user, is_active=True)
    else:
        session_id = request.session.get('chat_session_id')
        if not session_id:
            return JsonResponse({'messages': []})
        chat_session = ChatSession.objects.get(id=session_id)
    
    messages = ChatMessage.objects.filter(session=chat_session).order_by('-timestamp')[:50]
    return JsonResponse({'messages': list(messages.values())})

@csrf_exempt
def start_chat(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            chat_session, created = ChatSession.objects.get_or_create(user=request.user, is_active=True)
        else:
            guest_name = request.POST.get('guest_name')
            guest_email = request.POST.get('guest_email')
            if guest_name and guest_email:
                chat_session = ChatSession.objects.create(guest_name=guest_name, guest_email=guest_email)
                request.session['chat_session_id'] = chat_session.id
            else:
                return JsonResponse({'status': 'error', 'message': 'Name and email are required'})
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})