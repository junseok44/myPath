import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import Room, Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )


    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        sender_id = event["sender_id"]
        chat_id = event["chat_id"]

        await self.send(text_data=json.dumps({"message": message, "sender":sender, "sender_id":sender_id, "chat_id": chat_id}))

    async def chat_read_message(self,event):
        chat_id = event['chat_id']
        await database_sync_to_async(update_chat)(chat_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['type'] == "send_message":
            message = text_data_json["message"]
            sender = text_data_json["sender"]
            sender_id = text_data_json["sender_id"]
            chat_id = text_data_json["chat_id"]
            await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "chat_id":chat_id, "message": message, "sender": sender, "sender_id":sender_id})

        elif text_data_json['type'] == "read_message":
            chat_id = text_data_json["chat_id"]
            await self.channel_layer.group_send(self.room_group_name, {"type": "chat.read_message", "chat_id": chat_id})



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

    def room_read_and_update(self, event):
        self.send(text_data="{'hello': 'junseok'}")

    def receive(self,text_data):

        text_data_json = json.loads(text_data)
        if text_data_json['type'] == "update_room":
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "room.update_room_list"})



def get_user_room_list_json(userId):

    q1 = Room.objects.filter(startUser=userId, startUser_is_room_deleted=False)
    q2 = Room.objects.filter(endUser=userId, endUser_is_room_deleted=False)

    room_list = q1.union(q2, all=True).order_by('-lastMessageTime')

    room_list_data = []
    for room in room_list:

        unread_count = Chat.objects.filter(is_read=False,room=room,receiver=userId).count()
        room_data = {
            'id': str(room.id),
            'unread_count': unread_count,
            'startUser_id': str(room.startUser.id),
            'startUser_username': room.startUser.username,
            'endUser_id': str(room.endUser.id),
            'endUser_username': room.endUser.username,
            'lastMessageTime': str(room.lastMessageTime),
            'lastMessage': room.lastMessage,
        }
        room_list_data.append(room_data)

    return json.dumps(room_list_data)


def update_chat(chatId):
    Chat.objects.filter(id=chatId).update(is_read=True)


# 문자가 갔다는것. sender. receiver. 그리고 그때의 메시지. 그리고 그때의 시간.
# 그것을 가지고 해당 유저의 룸 리스트에 접속해서, 그걸 전송하면
# 그 유저의 룸 리스트에서 그걸 받는 사람은 그걸 받아서 자기 룸을 업데이트한다.
# 이때 기존 방이 있으면? 시간과 목록만 업데이트하는데. 기존 방이 없으면? 새로 만든다.
# 근데 이거를 기존거를 놔두고 자바스크립트로 업데이트할건지
# 아니면, send_message 이후 업데이트된 방 리스트를. 소켓으로 받을 것인지.