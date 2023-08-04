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
    username = models.CharField(max_length=20, unique=True)
    intro = models.CharField(max_length=300)
    membership = models.CharField(
        max_length=10, choices=membershipRank, default="bronze", blank=False, null=False)

    groups = models.ManyToManyField(
        AuthUser.groups.field.remote_field.model,
        related_name='custom_user_set',
        blank=True,
        help_text=_(
            "사용자가 속한 그룹입니다. 사용자는 각 그룹에 부여된 모든 권한을 받게 됩니다."
        ),
        verbose_name=_("groups"),
    )

    user_permissions = models.ManyToManyField(
        AuthUser.user_permissions.field.remote_field.model,
        related_name='custom_user_set',
        blank=True,
        help_text=_("사용자에 대한 특정 권한."),
        verbose_name=_("user permissions"),
    )
