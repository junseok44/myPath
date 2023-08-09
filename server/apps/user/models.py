from django.db import models
from django.contrib.auth.models import AbstractUser, User as AuthUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):

    membershipRank = [
        ('bronze', "브론즈"),
        ('silver', "실버"),
        ('gold', "골드"),
        ('platinum', "플래티넘"),
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    
    loginId = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "A user with that loginId already exists.",
        },
    )

    username = models.CharField(max_length=10, unique=True)

    email = models.EmailField(_('email address'), unique=True)

    intro = models.CharField(max_length=300)

    membership = models.CharField(
        max_length=10, choices=membershipRank, default="bronze", blank=False, null=False)
