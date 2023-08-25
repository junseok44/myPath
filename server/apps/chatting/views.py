from django.shortcuts import render
from apps.chatting.models import Room, Chat
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from apps.chatting.services import *
import json
# Create your views here.


User = get_user_model()

def view_rooms(request,other_id):
    other = User.objects.get(id=other_id)
    rooms = get_room_list(request.user,other)
    ctx = {
        "rooms": rooms
    }
    return render(request, 'chatting/rooms.html',ctx)

def ajax_get_room_chatting(request):
    
    data = json.loads(request.body)
    other_id = data['other_id']
    msg_list = get_message_list(request.user,other_id)

    return JsonResponse({"msg_list":msg_list})
        

def ajax_send_room_chatting(request):
    data = json.loads(request.body)
    other_id = data['other_id']
    message = data['message']
    other = User.objects.get(id=other_id)
    chat = send_message(request.user,other,message)

    return JsonResponse({"chat":chat})