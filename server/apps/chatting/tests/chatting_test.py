from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.chatting.services import send_message
from apps.chatting.models import Room,Chat
User = get_user_model()

class TestMessageSend(TestCase):
    def test_send_message(self):
        user1 = User.objects.create_user(username='startUser', password='1234', loginId="startUser1234")
        user2 = User.objects.create_user(username='endUser', password='1234', loginId="endUser1234")
        send_message(user1,user2,"안녕하세요")

        room = Room.objects.get()
        self.assertEqual(room.startUser,user1)
        self.assertEqual(room.endUser,user2)
        self.assertEqual(room.lastMessage,"안녕하세요")
        self.assertEqual(room.startUser_is_room_deleted,False)
        self.assertEqual(room.endUser_is_room_deleted,False)

        chat = Chat.objects.get()
        self.assertEqual(chat.sender,user1)
        self.assertEqual(chat.receiver,user2)
        self.assertEqual(chat.message,"안녕하세요")
        self.assertEqual(chat.leftUser,None)
        self.assertEqual(chat.room,room)
    
    def test_send_message_and_receive_message(self):
        self.test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room = Room.objects.get()
        initial_last_message_time = room.lastMessageTime

        send_message(user2,user1,"야 뭐라는거야")

        room = Room.objects.get()

        self.assertEqual(room.startUser,user1)
        self.assertEqual(room.endUser,user2)
        self.assertEqual(room.lastMessage,"야 뭐라는거야")
        self.assertEqual(room.startUser_is_room_deleted,False)
        self.assertEqual(room.endUser_is_room_deleted,False)
        self.assertNotEqual(room.lastMessageTime,initial_last_message_time)

        chat = Chat.objects.last()
        self.assertEqual(chat.sender,user2)
        self.assertEqual(chat.receiver,user1)
        self.assertEqual(chat.message,"야 뭐라는거야")
        self.assertEqual(chat.leftUser,None)
        self.assertEqual(chat.room,room)
    
        


