from django.shortcuts import render
from apps.chatting.models import Room, Chat
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
import json
# Create your views here.


User = get_user_model()

def view_rooms(request):
    user = request.user
    q1 = Room.objects.filter(Q(startUser=user) | Q(startUser_is_room_deleted=False))
    q2 = Room.objects.filter(Q(endUser=user) | Q(endUser_is_room_deleted=False))
    rooms = q1.union(q2).order_by('-lastMessageTime')
    ctx = {
        "rooms": rooms
    }
    return render(request, 'chatting/rooms.html',ctx)

def ajax_get_room_chatting(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        chats = Chat.objects.filter(room=room_id).order_by('-time')
        chats_list = []
        for chat in chats:
            # chat.leftUser 가 None이거나, 내가 아닐때. 불러온다.
            if chat.leftUser == None or chat.leftUser != request.user:
                chats_list.append(chat)
        chats_json = json.dumps([chat.to_json() for chat in chats_list])
        
    return JsonResponse({"chats": chats_json },200)
        


