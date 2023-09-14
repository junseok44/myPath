class Room(TimeStampedModel):
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    sender_unread_count = models.IntegerField("보낸 사람이 읽지 않은 개수")
    sender_is_deleted = models.BooleanField("보낸 사람이 지웠는지 여부")

    receiver_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    receiver_unread_count = models.IntegerField("받는 사람이 읽지 않은 개수")
    receiver_is_deleted = models.BooleanField("받는 사람이 지웠는지 여부")

    latest_text = models.CharField('마지막 메시지', max_length=1000)

class Message(TimeStampedModel):
    class VisibleChoices(models.TextChoices):
        BOTH = 'BOTH', '두 사람 모두 읽을 수 있음'
        ONLY_SENDER = 'ONLY_SENDER', '보낸 사람만 읽을 수 있음'
        ONLY_RECEIVER = 'ONLY_RECEIVER', '받는 사람만 읽을 수 있음'
        NOBODY = 'NOBODY', '모두 읽을 수 없음'

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_from_sender = models.BooleanField("보낸 사람이 메시지를 보냈는지 여부")
    text = models.CharField('메시지', max_length=1000)
    read = models.BooleanField('받는 사람이 읽음 여부')
    visible = models.CharField('읽을 수 있는 사람', max_length=16, choices=VisibleChoices.choices)