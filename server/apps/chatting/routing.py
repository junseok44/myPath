from django.urls import re_path
from apps.chatting.consumers import ChatConsumer, RoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/user_room/(?P<user_id>\w+)/$", RoomConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>[A-Za-z0-9_-]+', RoomConsumer.as_asgi())
]