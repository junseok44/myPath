from django.db import transaction
from apps.chatting.models import Room, Chat
from django.db.models import Q

@transaction.atomic
def send_message(sender, receiver, text):
    try:
        room = Room.objects.get(startUser=sender, endUser=receiver)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(startUser=receiver, endUser=sender)
        except Room.DoesNotExist:
            # 두 사람의 방이 없음.
            room = Room.objects.create(startUser=sender, endUser=receiver, lastMessage=text)
            chat = Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
        else:
            # receiver가 startUser인 방이 있음.
            chat = Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
    else:
        # sender가 startUser인 방이 있음.
        chat = Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
    room.lastMessage = text
    room.save()
    return {"sender":chat.sender, "receiver":chat.receiver, "time":chat.time, "message":chat.message, "room":chat.room}


def get_room_list(me):
    q1 = Room.objects.filter(startUser=me,startUser_is_room_deleted=False)
    q2 = Room.objects.filter(endUser=me,endUser_is_room_deleted=False)
    rooms = q1.union(q2).order_by('-lastMessageTime')
    return rooms


def get_message_list(me, other):
    try:
        room = Room.objects.get(startUser=me, endUser=other)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(startUser=other, endUser=me)
        except Room.DoesNotExist:
            # 두 사람의 방이 없음.
            return []

    return Chat.objects.filter(room=room).filter(Q(leftUser=None) | Q(leftUser=other)).order_by('-time')


def delete_room(me,other):
    try:
        room = Room.objects.get(startUser=me, endUser=other)
        if room.endUser_is_room_deleted:
            room.delete()
        else:
            room.startUser_is_room_deleted = True
            room.save()
            Chat.objects.filter(room=room).update(leftUser=me)
    except Room.DoesNotExist:
        try: 
            room = Room.objects.get(startUser=other, endUser=me)
            if room.startUser_is_room_deleted:
                room.delete()
            else:
                room.endUser_is_room_deleted = True
                room.save()
                Chat.objects.filter(room=room).update(leftUser=me)
        except Room.DoesNotExist:
            return False
    


