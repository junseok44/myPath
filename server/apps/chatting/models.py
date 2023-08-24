from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Room(models.Model):
    startUser = models.ForeignKey(User, models.CASCADE, related_name='start_room')
    endUser = models.ForeignKey(User, models.CASCADE, related_name='end_room')
    lastMessage = models.CharField(max_length=100)
    lastMessageTime = models.DateTimeField(auto_now=True)
    startUser_is_room_deleted = models.BooleanField(default=False)
    endUser_is_room_deleted = models.BooleanField(default=False)
    
# 만약 user 한명이 방을 나가면?? -> 방을 삭제하는게 아니라, 그냥 그 유저의 방 목록에서 안보이도록 해야함.

class Chat(models.Model):
    sender = models.ForeignKey(User,models.CASCADE, related_name='sender_chat')
    receiver = models.ForeignKey(User,models.CASCADE, related_name='receiver_chat')
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, models.CASCADE, related_name='room_chat')
    leftUser = models.ForeignKey(User, models.CASCADE, related_name='left_user_chat', null=True)
    
# 그 룸에 계속 있었던 사람은 -> 그 룸의 챗을 모두 불러온다.
# 그 룸에 나갔다가 들어온 사람은 -> 그 룸에서 새로 시작된 챗만 불러온다.


    
