@transaction.atomic
def send_message(sender: User, receiver: User, text: str):
    if sender == receiver:
        return

    # 1. 내가 보낸 사람으로 만든 채팅 방이 있는지 확인한다.
    try:
        room = Room.objects.get(sender_user=sender, receiver_user=receiver)
        is_sender = True

    except Room.DoesNotExist:
        # 2. 내가 받는 사람으로 만든 채팅 방이 있는지 확인한다.
        try:
            room = Room.objects.get(sender_user=receiver, receiver_user=sender)
            is_sender = False

        except Room.DoesNotExist:
            # 3. 내가 보낸 사람으로 채팅 방을 만든다.
            room = Room.objects.create(
                sender_user=sender,
                sender_unread_count=0,
                sender_is_deleted=False,
                receiver_user=receiver,
                receiver_unread_count=0,
                receiver_is_deleted=False,
            )
            is_sender = True

    if is_sender:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=False,
            read=False,
        ).update(read=True, modified=now())

        # 메시지 발신 처리
        message = Message.objects.create(
            room=room,
            is_from_sender=True,
            text=text,
            read=False,
            visible=Message.VisibleChoices.BOTH,
        )

        # 채팅 방 업데이트 처리
        room.sender_unread_count = 0
        room.sender_is_deleted = False
        room.receiver_unread_count += 1
        room.receiver_is_deleted = False
        room.latest_text = text
        room.save()

    else:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=True,
            read=False,
        ).update(read=True, modified=now())

        # 메시지 발신 처리
        message = Message.objects.create(
            room=room,
            is_from_sender=False,
            text=text,
            read=False,
            visible=Message.VisibleChoices.BOTH,
        )

        # 채팅 방 업데이트 처리
        room.sender_unread_count += 1
        room.sender_is_deleted = False
        room.receiver_unread_count = 0
        room.receiver_is_deleted = False
        room.latest_text = text
        room.save()



@transaction.atomic
def delete_room(me: User, other: User):
    # 1. 내가 보낸 사람으로 만든 채팅 방이 있는지 확인한다.
    try:
        room = Room.objects.get(sender_user=me, receiver_user=other)
        is_sender = True

    except Room.DoesNotExist:
        # 2. 내가 받는 사람으로 만든 채팅 방이 있는지 확인한다.
        try:
            room = Room.objects.get(sender_user=other, receiver_user=me)
            is_sender = False

        except Room.DoesNotExist:
            return

    if is_sender:
        # 읽음 처리는 안함
        # 메시지 삭제 처리 - 상대방이 삭제 아직 안한 경우
        Message.objects.filter(
            room=room,
            visible=Message.VisibleChoices.BOTH,
        ).update(
            visible=Message.VisibleChoices.ONLY_RECEIVER,
            modified=now(),
        )
        # 메시지 삭제 처리 - 상대방이 이미 삭제한 경우
        Message.objects.filter(
            room=room,
            visible=Message.VisibleChoices.ONLY_SENDER,
        ).update(
            visible=Message.VisibleChoices.NOBODY,
            modified=now(),
        )

        # 대화방 비활성화
        room.sender_unread_count = 0
        room.sender_is_deleted = True
        room.save()

    else:
        # 읽음 처리는 안함
        # 메시지 삭제 처리 - 상대방이 삭제 아직 안한 경우
        Message.objects.filter(
            room=room,
            visible=Message.VisibleChoices.BOTH,
        ).update(
            visible=Message.VisibleChoices.ONLY_SENDER,
            modified=now(),
        )
        # 메시지 삭제 처리 - 상대방이 이미 삭제한 경우
        Message.objects.filter(
            room=room,
            visible=Message.VisibleChoices.ONLY_RECEIVER,
        ).update(
            visible=Message.VisibleChoices.NOBODY,
            modified=now(),
        )

        # 대화방 비활성화
        room.receiver_unread_count = 0
        room.receiver_is_deleted = True
        room.save()


def get_room_list(user: User):
    q1 = Room.objects.filter(sender_user=user, sender_is_deleted=False).annotate(
        user=F('receiver_user'),
        unread_count=F('sender_unread_count'),
    ).values('user', 'unread_count', 'latest_text', 'modified')

    q2 = Room.objects.filter(receiver_user=user, receiver_is_deleted=False).annotate(
        user=F('sender_user'),
        unread_count=F('receiver_unread_count'),
    ).values('user', 'unread_count', 'latest_text', 'modified')

    return q1.union(q2, all=True).order_by('-modified')



@transaction.atomic
def get_message_list(me: User, other: User):
    try:
        room = Room.objects.get(sender_user=me, receiver_user=other)
        is_sender = True

    except Room.DoesNotExist:
        # 여기서 실패하면 raise
        room = Room.objects.get(sender_user=other, receiver_user=me)
        is_sender = False

    if is_sender:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=False,
            read=False,
        ).update(read=True, modified=now())

        # 대화방 읽음 처리
        room.sender_unread_count = 0
        room.save()

        # 내가보낸 메시지는 항상 나는 읽었음 -> 안궁금함
        # 내가보낸 메시지를 저사람이 읽었는가??? 그것이 궁금한것임.
        # 상대방이 보낸 메시지는 항상 상대방이 읽었음
        # 내가 보낸 메시지만 적용하면됨
        return Message.objects.filter(
            room=room,
            visible__in=(Message.VisibleChoices.BOTH, Message.VisibleChoices.ONLY_SENDER),
        ).annotate(
            sent_by_me=F('is_from_sender'),  # 반대에는 Not 붙이기
            was_read=Case(
                When(is_from_sender=True, then=F('read')),
                default=True,
            )
        ).values('id', 'sent_by_me', 'was_read', 'text', 'created').order_by('-id')

    else:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=True,
            read=False,
        ).update(read=True, modified=now())

        # 대화방 읽음 처리
        room.receiver_unread_count = 0
        room.save()

        # 내가보낸 메시지는 항상 나는 읽었음 -> 안궁금함
        # 내가보낸 메시지를 저사람이 읽었는가??? 그것이 궁금한것임.
        # 상대방이 보낸 메시지는 항상 상대방이 읽었음
        # 내가 보낸 메시지만 적용하면됨
        return Message.objects.filter(
            room=room,
            visible__in=(Message.VisibleChoices.BOTH, Message.VisibleChoices.ONLY_RECEIVER),
        ).annotate(
            sent_by_me=Case(When(is_from_sender=False, then=True), default=False),  # not 지원안함 -- case when으로 때움
            was_read=Case(
                When(is_from_sender=False, then=F('read')),
                default=True,
            )
        ).values('id', 'sent_by_me', 'was_read', 'text', 'created').order_by('-id')