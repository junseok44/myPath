from django.test import TestCase

from message.models import Room, Message
from message.services import send_message, delete_room, get_room_list, get_message_list
from users.models import User

class TestMessageSend(TestCase):
    def test_send(self):
        # Given: 보낸 사람, 받는 사람 생성
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'

        # When: sender -> receiver 메시지 발송
        send_message(sender, receiver, text)

        # Then: 방이 잘 만들어짐
        room = Room.objects.get()
        self.assertEqual(room.sender_user, sender)
        self.assertEqual(room.sender_unread_count, 0)
        self.assertEqual(room.sender_is_deleted, False)
        self.assertEqual(room.receiver_user, receiver)
        self.assertEqual(room.receiver_unread_count, 1)
        self.assertEqual(room.receiver_is_deleted, False)
        self.assertEqual(room.latest_text, text)

        # Then: 메시지가 잘 보내짐
        message = Message.objects.get()
        self.assertEqual(message.room, room)
        self.assertEqual(message.is_from_sender, True)
        self.assertEqual(message.text, text)
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.BOTH)

    def test_send_and_receive(self):
        # Given: sender -> receiver 으로 전송
        self.test_send()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')
        text = 'message from receiver to sender'

        # When: receiver -> sender 메시지 발송
        send_message(receiver, sender, text)

        # Then: 방이 잘 업데이트됨
        room = Room.objects.get()
        self.assertEqual(room.sender_user, sender)
        self.assertEqual(room.sender_unread_count, 1)
        self.assertEqual(room.sender_is_deleted, False)
        self.assertEqual(room.receiver_user, receiver)
        self.assertEqual(room.receiver_unread_count, 0)
        self.assertEqual(room.receiver_is_deleted, False)
        self.assertEqual(room.latest_text, text)

        # Then: 메시지가 잘 보내짐
        message = Message.objects.last()
        self.assertEqual(message.room, room)
        self.assertEqual(message.is_from_sender, False)
        self.assertEqual(message.text, text)
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.BOTH)

        # Then: 이전 메시지가 읽음 처리 됨
        message = Message.objects.first()
        self.assertEqual(message.read, True)

    def test_send_and_receive_and_send(self):
        # Given: sender -> receiver -> sender 으로 전송
        self.test_send_and_receive()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')
        text = 'message from sender to receiver 2'

        # When: sender -> receiver 메시지 발송
        send_message(sender, receiver, text)

        # Then: 방이 잘 업데이트됨
        room = Room.objects.get()
        self.assertEqual(room.sender_user, sender)
        self.assertEqual(room.sender_unread_count, 0)
        self.assertEqual(room.sender_is_deleted, False)
        self.assertEqual(room.receiver_user, receiver)
        self.assertEqual(room.receiver_unread_count, 1)
        self.assertEqual(room.receiver_is_deleted, False)
        self.assertEqual(room.latest_text, text)

        # Then: 메시지가 잘 보내짐
        message = Message.objects.last()
        self.assertEqual(message.room, room)
        self.assertEqual(message.is_from_sender, True)
        self.assertEqual(message.text, text)
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.BOTH)

        # Then: 이전 메시지가 읽음 처리 됨
        message = Message.objects.all()[1]
        self.assertEqual(message.read, True)

class TestRoomRemove(TestCase):
    def test_send_and_remove_by_sender(self):
        # Given: 메시지 전송
        TestMessageSend().test_send()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')

        # sender_unread_count 강제로 임의로 설정
        Room.objects.all().update(sender_unread_count=1)

        # When: sender 가 삭제
        delete_room(sender, receiver)

        # Then: 삭제 처리됨 ; 방은 삭제처리, 메시지 ONLY_RECEIVER 삭제처리됨
        message = Message.objects.get()
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.ONLY_RECEIVER)

        # sender 만 제거됨
        room = Room.objects.get()
        self.assertEqual(room.sender_unread_count, 0)  # 강제로 0 셋팅 확인
        self.assertEqual(room.sender_is_deleted, True)

        # receiver 제거안됨
        self.assertEqual(room.receiver_unread_count, 1)
        self.assertEqual(room.receiver_is_deleted, False)

    def test_send_and_remove_by_receiver(self):
        # Given: 메시지 전송
        TestMessageSend().test_send()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')

        # receiver_unread_count 강제로 임의로 설정
        Room.objects.all().update(receiver_unread_count=1)

        # When: receiver 가 삭제 (안읽씹)
        delete_room(receiver, sender)

        # Then: 삭제 처리됨 ; 방은 삭제처리, 메시지 ONLY_SENDER 삭제처리됨
        message = Message.objects.get()
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.ONLY_SENDER)

        # sender 제거안됨
        room = Room.objects.get()
        self.assertEqual(room.sender_unread_count, 0)
        self.assertEqual(room.sender_is_deleted, False)

        # receiver 제거처리
        self.assertEqual(room.receiver_unread_count, 0)
        self.assertEqual(room.receiver_is_deleted, True)

    def test_send_and_remove_by_sender_and_remove_by_receiver(self):
        # Given
        self.test_send_and_remove_by_sender()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')

        # receiver_unread_count 강제로 임의로 설정
        Room.objects.all().update(receiver_unread_count=1)

        # When
        delete_room(receiver, sender)

        # Then: 삭제 처리됨 ; 방은 삭제처리, 메시지 NOBODY 삭제처리됨
        message = Message.objects.get()
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.NOBODY)

        # sender 제거됨
        room = Room.objects.get()
        self.assertEqual(room.sender_unread_count, 0)
        self.assertEqual(room.sender_is_deleted, True)

        # receiver 제거처리
        self.assertEqual(room.receiver_unread_count, 0)  # updated
        self.assertEqual(room.receiver_is_deleted, True)

    def test_send_and_remove_by_receiver_and_remove_by_sender(self):
        self.test_send_and_remove_by_receiver()
        sender = User.objects.get(username='sender')
        receiver = User.objects.get(username='receiver')

        # sender_unread_count 강제로 임의로 설정
        Room.objects.all().update(sender_unread_count=1)

        # When
        delete_room(sender, receiver)

        # Then: 삭제 처리됨 ; 방은 삭제처리, 메시지 NOBODY 삭제처리됨
        message = Message.objects.get()
        self.assertEqual(message.read, False)
        self.assertEqual(message.visible, Message.VisibleChoices.NOBODY)

        # sender 제거됨
        room = Room.objects.get()
        self.assertEqual(room.sender_unread_count, 0)
        self.assertEqual(room.sender_is_deleted, True)

        # receiver 제거처리
        self.assertEqual(room.receiver_unread_count, 0)
        self.assertEqual(room.receiver_is_deleted, True)

class TestGetRoomList(TestCase):
    def test_send_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 receiver가 보임
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            [{'latest_text': 'message from sender to receiver', 'user': receiver.id, 'unread_count': 0}]
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 보임
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            [{'latest_text': 'message from sender to receiver', 'user': sender.id, 'unread_count': 1}]
        )

    def test_send_and_reply_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        text2 = 'message from receiver to sender'
        send_message(receiver, sender, text2)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 receiver이 보임
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            [{'latest_text': 'message from receiver to sender', 'user': receiver.id, 'unread_count': 1}]
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 보임
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            [{'latest_text': 'message from receiver to sender', 'user': sender.id, 'unread_count': 0}]
        )

    def test_send_and_remove_by_sender_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(sender, receiver)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 보이지 않음 (삭제했으므로)
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            []
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 보임
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            [{'latest_text': 'message from sender to receiver', 'user': sender.id, 'unread_count': 1}]
        )

    def test_send_and_remove_by_receiver_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(receiver, sender)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 receiver가 보임
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            [{'latest_text': 'message from sender to receiver', 'user': receiver.id, 'unread_count': 0}]
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 안보임 (삭제했으므로)
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            []
        )

    def test_send_and_remove_by_sender_and_remove_by_receiver_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(receiver, sender)
        delete_room(sender, receiver)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 receiver가 안보임 (삭제했으므로)
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            []
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 안보임 (삭제했으므로)
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            []
        )

    def test_send_and_remove_by_sender_and_remove_by_receiver_and_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(sender, receiver)
        delete_room(receiver, sender)

        # When: sender 가 메시지 읽음
        sender_result = get_room_list(sender)

        # Then: sender에게는 receiver가 안보임 (삭제했으므로)
        sender_result = list(sender_result)
        for d in sender_result:
            del d['modified']
        self.assertEqual(
            sender_result,
            []
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_room_list(receiver)

        # Then: receiver에게는 sender이 안보임 (삭제했으므로)
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['modified']
        self.assertEqual(
            receiver_result,
            []
        )

class TestGetMessageList(TestCase):
    def test_send_and_get_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)

        # When: sender 가 메시지 읽음
        self.assertEqual(Room.objects.get().sender_unread_count, 0)
        self.assertEqual(Room.objects.get().receiver_unread_count, 1)
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': True, 'was_read': False}]
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_message_list(receiver, sender)
        self.assertEqual(Room.objects.get().sender_unread_count, 0)
        self.assertEqual(Room.objects.get().receiver_unread_count, 0)

        # Then: 메시지 정상적으로 불러옴
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': False, 'was_read': True}]
        )

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)
        self.assertEqual(Room.objects.get().sender_unread_count, 0)
        self.assertEqual(Room.objects.get().receiver_unread_count, 0)

        # Then: 메시지 정상적으로 불러옴 - was_read 업데이트됨
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': True, 'was_read': True}]
        )

    def test_send_and_reply_and_get_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        text2 = 'message from receiver to sender'
        send_message(receiver, sender, text2)

        # When: receiver 가 메시지 읽음
        self.assertEqual(Room.objects.get().sender_unread_count, 1)
        self.assertEqual(Room.objects.get().receiver_unread_count, 0)
        receiver_result = get_message_list(receiver, sender)

        # Then: 메시지 정상적으로 불러옴
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            [{'id': 2, 'text': 'message from receiver to sender', 'sent_by_me': True, 'was_read': False},
             {'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': False, 'was_read': True}]
        )
        self.assertEqual(Room.objects.get().sender_unread_count, 1)
        self.assertEqual(Room.objects.get().receiver_unread_count, 0)

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            [{'id': 2, 'text': 'message from receiver to sender', 'sent_by_me': False, 'was_read': True},
             {'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': True, 'was_read': True}]
        )
        self.assertEqual(Room.objects.get().sender_unread_count, 0)
        self.assertEqual(Room.objects.get().receiver_unread_count, 0)

        # When: 다시 receiver 가 메시지 읽음
        receiver_result = get_message_list(receiver, sender)

        # Then: 메시지 정상적으로 불러옴 - was_read 업데이트됨
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            [{'id': 2, 'text': 'message from receiver to sender', 'sent_by_me': True, 'was_read': True},
             {'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': False, 'was_read': True}]
        )

class TestGetMessageListAfterRemove(TestCase):
    def test_send_and_remove_by_sender_and_get_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송, sender 메시지 삭제
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(sender, receiver)

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            []
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_message_list(receiver, sender)

        # Then: 메시지 정상적으로 불러옴
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': False, 'was_read': True}]
        )

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴 - was_read 업데이트됨
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            []
        )

    def test_send_and_remove_by_receiver_and_get_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(receiver, sender)

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': True, 'was_read': False}]
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_message_list(receiver, sender)

        # Then: 메시지 정상적으로 불러옴
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            []
        )

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴 - was_read 업데이트됨
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            [{'id': 1, 'text': 'message from sender to receiver', 'sent_by_me': True, 'was_read': True}]
        )

    def test_send_and_remove_by_both_and_get_read(self):
        # Given: 보낸 사람, 받는 사람 생성; sender -> receiver 메시지 발송
        sender = User.objects.create_user('sender')
        receiver = User.objects.create_user('receiver')
        text = 'message from sender to receiver'
        send_message(sender, receiver, text)
        delete_room(receiver, sender)
        delete_room(sender, receiver)

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            []
        )

        # When: receiver 가 메시지 읽음
        receiver_result = get_message_list(receiver, sender)

        # Then: 메시지 정상적으로 불러옴
        receiver_result = list(receiver_result)
        for d in receiver_result:
            del d['created']
        self.assertEqual(
            receiver_result,
            []
        )

        # When: sender 가 메시지 읽음
        sender_result = get_message_list(sender, receiver)

        # Then: 메시지 정상적으로 불러옴 - was_read 업데이트됨
        sender_result = list(sender_result)
        for d in sender_result:
            del d['created']
        self.assertEqual(
            sender_result,
            []
        )