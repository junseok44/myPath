import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room
from django.db.models import Q
from django.core import serializers

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        sender_id = event["sender_id"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "sender":sender, "sender_id":sender_id}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        sender_id = text_data_json["sender_id"]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "sender": sender, "sender_id":sender_id})

        # self.send(text_data=json.dumps({"message": message}))



class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"room_{self.user_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        room_list_json=get_user_room_list_json(self.user_id)
        self.send(text_data=room_list_json)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def room_update_room_list(self, event):
        room_list_json=get_user_room_list_json(self.user_id)
        self.send(text_data=room_list_json)

    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "room.update_room_list"})
        


def get_user_room_list_json(userId):

    q1 = Room.objects.filter(startUser=userId, startUser_is_room_deleted=False)
    q2 = Room.objects.filter(endUser=userId, endUser_is_room_deleted=False)

    room_list = q1.union(q2, all=True).order_by('-lastMessageTime')
    room_list_data = []
    for room in room_list:
        room_data = {
            'id': str(room.id),
            'startUser_id': str(room.startUser.id),
            'startUser_username': room.startUser.username,
            'endUser_id': str(room.endUser.id),
            'endUser_username': room.endUser.username,
            'lastMessageTime': str(room.lastMessageTime),
            'lastMessage': room.lastMessage,
        }
        room_list_data.append(room_data)
    # room_list_json = json.loads(serializers.serialize('json', room_list, fields=('id', 'startUser', 'endUser', 'startUser__username',"endUser__username",'lastMessageTime', 'lastMessage')))

    return json.dumps(room_list_data)


# 문자가 갔다는것. sender. receiver. 그리고 그때의 메시지. 그리고 그때의 시간.
# 그것을 가지고 해당 유저의 룸 리스트에 접속해서, 그걸 전송하면
# 그 유저의 룸 리스트에서 그걸 받는 사람은 그걸 받아서 자기 룸을 업데이트한다.
# 이때 기존 방이 있으면? 시간과 목록만 업데이트하는데. 기존 방이 없으면? 새로 만든다.
# 근데 이거를 기존거를 놔두고 자바스크립트로 업데이트할건지
# 아니면, send_message 이후 업데이트된 방 리스트를. 소켓으로 받을 것인지.