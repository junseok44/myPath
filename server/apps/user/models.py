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

    profile=models.ImageField(upload_to="user/", default="/resource/noimage.jpg")

    intro = models.CharField(max_length=300)

    membership = models.CharField(
        max_length=10, choices=membershipRank, default="bronze", blank=False, null=False)
    
    kakaoId = models.CharField(null=True,blank=True, max_length=30)
    googleId = models.CharField(null=True,blank=True, max_length=30)
    naverId = models.CharField(null=True,blank=True, max_length=30)





class UserCard(models.Model):
    title = models.CharField(max_length=20)
    link = models.CharField(null=True, blank=True, max_length=100)
    desc = models.CharField(max_length=100)
    writer = models.ForeignKey(User, models.CASCADE, related_name="user_card")
    # profile=models.ImageField(upload_to="user/",blank=True,null=True)