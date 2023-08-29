from django.shortcuts import render, redirect
from apps.chatting.models import Room, Chat
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from apps.chatting.services import *
from django.core import serializers
import json
# Create your views here.


User = get_user_model()

def view_rooms(request):
    ctx = {
        "rooms": get_room_list(request.user)
    }
    return render(request, 'chatting/rooms.html',ctx)

def view_chats(request,other_id):
    other = User.objects.get(id=other_id)

    msg_list = get_message_list(request.user,other)

    if len(msg_list) > 10:
        msg_list = msg_list[len(msg_list)-10:]
    ctx = {
        "other": other,
        "msg_list": msg_list,
        "current_room": get_current_room(request.user,other)
    }
    return render(request, 'chatting/chats.html',ctx)



def ajax_get_room_message(request):
    
    global messageIndex
    data = json.loads(request.body)
    other_id = data['other_id']
    messageIndex = data['messageIndex']
    msg_list = get_message_list(request.user,other_id)


    # 가령 11개에서 20개까지 보여준다고 하면.
    #메시지가 10개 이하일때.
    if len(msg_list)-10*(messageIndex-1) <= 0:
        return JsonResponse({"msg_list":[]})
    # 메시지가 11개 이상 20개 이하일때.
    elif len(msg_list)-10*(messageIndex) < 0:
        msg_list = msg_list[0:len(msg_list) - 10*(messageIndex-1)]
        return JsonResponse({"msg_list":get_message_list_data(msg_list)})
    # 메시지가 21개 이상 30개 이하일때.
    else:
        msg_list = msg_list[len(msg_list) - 10*(messageIndex):len(msg_list)-10*(messageIndex-1)]
        return JsonResponse({"msg_list":get_message_list_data(msg_list)})

        
def ajax_send_room_message(request):
    data = json.loads(request.body)
    receiver_id = data['receiver']
    text = data['text']
    receiver = User.objects.get(id=receiver_id)
    try:
        chat = send_message(request.user,receiver,text)
        return JsonResponse({"chat":chat, "receiver_id": receiver_id})
    except Exception as e:
        print(e)
        return JsonResponse({"error":"error"},status=400)
    
def ajax_delete_room(request, other_id):
    if request.method == "POST":
        other = User.objects.get(id=other_id)
        delete_room(request.user,other)
        return redirect('/chat/rooms')
    else:
        return HttpResponseNotAllowed(['POST'])