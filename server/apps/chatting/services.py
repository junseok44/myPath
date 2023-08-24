from django.db import transaction
from apps.chatting.models import Room, Chat

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
            Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
        else:
            # receiver가 startUser인 방이 있음.
            Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
    else:
        # sender가 startUser인 방이 있음.
        Chat.objects.create(sender=sender, receiver=receiver, message=text, room=room)
    room.lastMessage = text
    room.save()

