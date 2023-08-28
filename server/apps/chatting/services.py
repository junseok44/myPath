from django.db import transaction
from apps.chatting.models import Room, Chat
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()


@transaction.atomic
def send_message(sender, receiver, text):
    if sender == receiver:
        raise Exception("자기 자신에게는 메시지를 보낼 수 없습니다.")
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
    room.endUser_is_room_deleted = False
    room.startUser_is_room_deleted = False
    room.lastMessage = text
    room.save()

    async_to_sync(channel_layer.group_send)(
        f"chat_{room.id}", {"type": "chat.message", "chat_id":chat.id, "message": chat.message, "sender": sender.username, "sender_id": str(chat.sender.id)}
    )

    return {"chat_id": chat.id, "sender":chat.sender.username, "receiver":chat.receiver.username, "time":chat.time, "message":chat.message}


def get_room_list(me):
    q1 = Room.objects.filter(startUser=me,startUser_is_room_deleted=False)
    q2 = Room.objects.filter(endUser=me,endUser_is_room_deleted=False)
    rooms = q1.union(q2).order_by('-lastMessageTime')
    print(rooms)
    return rooms


def get_current_room(me, other):
    try:
        room = Room.objects.get(startUser=me, endUser=other)
        return room
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(startUser=other, endUser=me)
            return room
        except Room.DoesNotExist:
            return None


def get_message_list(me, other):
    try:
        room = Room.objects.get(startUser=me, endUser=other)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(startUser=other, endUser=me)
        except Room.DoesNotExist:
            # 두 사람의 방이 없음.
            return []

    q1 = Chat.objects.filter(room=room,leftUser=None)
    q2 = Chat.objects.filter(room=room,leftUser=other)

    q1.filter(receiver=me).update(is_read=True)
    q2.filter(receiver=me).update(is_read=True)

    return q1.union(q2).order_by('time')


def delete_room(me,other):
    try:
        room = Room.objects.get(startUser=me, endUser=other)
        if room.endUser_is_room_deleted:
            room.delete()
        else:
            room.startUser_is_room_deleted = True
            room.save()
            for chat in Chat.objects.filter(room=room):
                if chat.leftUser == None:
                    chat.leftUser = me
                    chat.save()
                elif chat.leftUser == other:
                    chat.delete()
    except Room.DoesNotExist:
        try: 
            room = Room.objects.get(startUser=other, endUser=me)
            if room.startUser_is_room_deleted:
                room.delete()
            else:
                room.endUser_is_room_deleted = True
                room.save()
                for chat in Chat.objects.filter(room=room):
                    if chat.leftUser == None:
                        chat.leftUser = me
                        chat.save()
                    elif chat.leftUser == other:
                        chat.delete()
        except Room.DoesNotExist:
            return False
    


