from django.shortcuts import path,include


urlpatterns = [
    path('rooms/', view_rooms,name='rooms'),
    path('api/send_chatting', ajax_send_room_chatting, name='chatting'),
    path('api/get_chatting', ajax_get_room_chatting, name='chatting'),
]