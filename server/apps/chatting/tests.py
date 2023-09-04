from django.test import TestCase
from apps.chatting.services import get_message_list
from django.contrib.auth import get_user_model
from apps.chatting.services import *
from apps.chatting.models import Room,Chat
from django.core.exceptions import ObjectDoesNotExist

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
        initial_message = room.lastMessage
        initial_last_message_time = room.lastMessageTime

        send_message(user2,user1,"야 뭐라는거야")
        room = Room.objects.get()

        self.assertEqual(room.startUser,user1)
        self.assertEqual(room.endUser,user2)
        self.assertEqual(room.lastMessage,"야 뭐라는거야")
        self.assertEqual(room.startUser_is_room_deleted,False)
        self.assertEqual(room.endUser_is_room_deleted,False)
        self.assertNotEqual(initial_message,room.lastMessage)
        self.assertNotEqual(room.lastMessageTime,initial_last_message_time)

        chat = Chat.objects.last()
        self.assertEqual(chat.sender,user2)
        self.assertEqual(chat.receiver,user1)
        self.assertEqual(chat.message,"야 뭐라는거야")
        self.assertEqual(chat.leftUser,None)
        self.assertEqual(chat.room,room)

class TestRoomExit(TestCase):
    # 유저가 방을 나갔을때 chat의 leftUesr는 user로 등록되고, room의
    def test_start_user_room_exit(self):
        TestMessageSend().test_send_message()
        room = Room.objects.get()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user1,user2)
        room = Room.objects.get()
        self.assertEqual(room.startUser_is_room_deleted,True)
        self.assertEqual(room.endUser_is_room_deleted,False)

        chat = Chat.objects.get()
        self.assertEqual(chat.leftUser, user1)

    def test_end_user_Room_exit(self):
        TestMessageSend().test_send_message()
        room = Room.objects.get()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user2,user1)
        room = Room.objects.get()
        self.assertEqual(room.startUser_is_room_deleted,False)
        self.assertEqual(room.endUser_is_room_deleted,True)
        
        chat = Chat.objects.get()
        self.assertEqual(chat.leftUser, user2)

    def test_startuser_exit_and_enduser_exit(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user1,user2)
        delete_room(user2,user1)
        with self.assertRaises(ObjectDoesNotExist):
            Room.objects.get()
        
        with self.assertRaises(ObjectDoesNotExist):
            Chat.objects.get()
        
    def test_startuser_exit_and_enduser_exit(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user2,user1)
        delete_room(user1,user2)
        with self.assertRaises(ObjectDoesNotExist):
            Room.objects.get()
        
        with self.assertRaises(ObjectDoesNotExist):
            Chat.objects.get()

#나가고 나서 방이 안보이는지 테스트해야함.
class TestGetRoomList(TestCase):
    def test_get_room_list(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user1)
        self.assertEqual(len(room_list),1)
        self.assertEqual(room_list[0].startUser,user1)
        self.assertEqual(room_list[0].endUser,user2)
        self.assertEqual(room_list[0].lastMessage,"안녕하세요")
        self.assertEqual(room_list[0].startUser_is_room_deleted,False)
        self.assertEqual(room_list[0].endUser_is_room_deleted,False)
    
    def test_get_room_list_after_startuser_exit(self):
        TestRoomExit().test_start_user_room_exit()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user1)
        room_list2 = get_room_list(user2)
        self.assertEqual(len(room_list),0)
        self.assertEqual(len(room_list2),1)

    def test_get_room_list_after_enduser_exit(self):
        TestRoomExit().test_end_user_Room_exit()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user2)
        self.assertEqual(len(room_list),0)
        room_list2 = get_room_list(user1)
        self.assertEqual(len(room_list2),1) 

    def test_get_startuser_room_after_enduser_exit(self):
        TestRoomExit().test_end_user_Room_exit()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user1)
        self.assertEqual(len(room_list),1)
        self.assertEqual(room_list[0].startUser,user1)
        self.assertEqual(room_list[0].endUser,user2)
        self.assertEqual(room_list[0].lastMessage,"안녕하세요")
        self.assertEqual(room_list[0].startUser_is_room_deleted,False)
        self.assertEqual(room_list[0].endUser_is_room_deleted,True)

    def test_get_enduser_room_after_startuser_exit(self):
        TestRoomExit().test_start_user_room_exit()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user2)
        self.assertEqual(len(room_list),1)
        self.assertEqual(room_list[0].startUser,user1)
        self.assertEqual(room_list[0].endUser,user2)
        self.assertEqual(room_list[0].lastMessage,"안녕하세요")
        self.assertEqual(room_list[0].startUser_is_room_deleted,True)
        self.assertEqual(room_list[0].endUser_is_room_deleted,False)

    def test_get_room_list_after_both_exit(self):
        TestRoomExit().test_startuser_exit_and_enduser_exit()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        room_list = get_room_list(user2)
        self.assertEqual(len(room_list),0)
        room_list2 = get_room_list(user1)
        self.assertEqual(len(room_list2),0)

class TestGetMessage(TestCase):
    def test_get_message(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        message_list = get_message_list(user1,user2)
        self.assertEqual(len(message_list),1)
        self.assertEqual(message_list[0].sender,user1)
        self.assertEqual(message_list[0].receiver,user2)
        self.assertEqual(message_list[0].message,"안녕하세요")
    # 메시지를 여러개 보냈을때, 10개만 받아야 함.
    def test_get_message_multiple(self):
        for i in range(15):
            TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')

        message_list = get_message_list(user1,user2)
        self.assertEqual(len(message_list),10)
        self.assertEqual(message_list[0].sender,user1)
        self.assertEqual(message_list[0].receiver,user2)
        self.assertEqual(message_list[0].message,"안녕하세요")
        self.assertEqual(message_list[9].sender,user1)
        self.assertEqual(message_list[9].receiver,user2)
        self.assertEqual(message_list[9].message,"안녕하세요")

class Test_Chat_Status_When_Exit(TestCase):
    def test_send_and_sender_exit(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user1,user2)

        user1_message = get_message_list(user1,user2)
        user2_message = get_message_list(user2,user1)

        self.assertEqual(len(user1_message),0)
        self.assertEqual(len(user2_message),1)
        self.assertEqual(user2_message[0].sender,user1)
        self.assertEqual(user2_message[0].receiver,user2)
        self.assertEqual(user2_message[0].message,"안녕하세요")

    def test_send_and_receiver_exit(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user2,user1)

        user1_message = get_message_list(user1,user2)
        user2_message = get_message_list(user2,user1)
        self.assertEqual(len(user1_message),1)
        self.assertEqual(len(user2_message),0)
        self.assertEqual(user1_message[0].sender,user1)
        self.assertEqual(user1_message[0].receiver,user2)
        self.assertEqual(user1_message[0].message,"안녕하세요")

    # 리시버에게는 마지막 메시지만 보여야함.
    def test_send_and_receiver_exit_and_sender_send(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user2,user1)
        send_message(user1,user2,"뭐라는거야")

        message_list = get_message_list(user1,user2)
        self.assertEqual(len(message_list),2)
        self.assertEqual(message_list[0].sender,user1)
        self.assertEqual(message_list[0].receiver,user2)
        self.assertEqual(message_list[0].message,"안녕하세요")

        self.assertEqual(message_list[1].sender,user1)
        self.assertEqual(message_list[1].receiver,user2)
        self.assertEqual(message_list[1].message,"뭐라는거야")

        message_list = get_message_list(user2,user1)
        self.assertEqual(len(message_list),1)
        self.assertEqual(message_list[0].sender,user1)
        self.assertEqual(message_list[0].receiver,user2)
        self.assertEqual(message_list[0].message,"뭐라는거야")

    def test_send_and_sender_exit_and_receiver_send(self):
        TestMessageSend().test_send_message()
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user1,user2)
        send_message(user2,user1,"뭐라는거야")

        message_list = get_message_list(user1,user2)
        self.assertEqual(len(message_list),1)
        self.assertEqual(message_list[0].sender,user2)
        self.assertEqual(message_list[0].receiver,user1)
        self.assertEqual(message_list[0].message,"뭐라는거야")
    
    def test_send_and_sender_exit_and_sender_send(self):
        TestMessageSend().test_send_message()   
        user1 = User.objects.get(username='startUser')
        user2 = User.objects.get(username='endUser')
        delete_room(user1,user2)
        send_message(user1,user2,"뭐라는거야")

        user1_message = get_message_list(user1,user2)
        user2_message = get_message_list(user2,user1)
        
        self.assertEqual(len(user1_message),1)
        self.assertEqual(len(user2_message),2)
        self.assertEqual(user1_message[0].sender,user1)
        self.assertEqual(user1_message[0].receiver,user2)
        self.assertEqual(user1_message[0].message,"뭐라는거야")
        self.assertEqual(user2_message[0].sender,user1)
        self.assertEqual(user2_message[0].receiver,user2)
        self.assertEqual(user2_message[0].message,"안녕하세요")
        self.assertEqual(user2_message[1].sender,user1)
        self.assertEqual(user2_message[1].receiver,user2)
        self.assertEqual(user2_message[1].message,"뭐라는거야")

