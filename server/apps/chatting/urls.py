from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/', view_rooms,name='rooms'),
    path('chats/<uuid:other_id>/',view_chats,name='chats'),
    path('api/send_message',ajax_send_room_message , name='send_message'),
    path('api/get_message', ajax_get_room_message, name='get_messages'),
    path('api/delete_room/<uuid:other_id>', ajax_delete_room, name='delete_room'),
]