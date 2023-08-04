from django.db import models
from apps.post.models import Post,Step
from apps.user.models import User

# Create your models here.


class PostComment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="post_comment")
    writer= models.ForeignKey(User, models.CASCADE, related_name="post_comment")
    text = models.CharField(max_length=100)
    parentComment = models.ForeignKey('self', models.CASCADE, null=True, blank=True)

class StepComment(models.Model):
    step = models.ForeignKey(Step,models.CASCADE, related_name='step_comment')
    writer= models.ForeignKey(User, models.CASCADE, related_name="step_comment")
    text = models.CharField(max_length=100)
    parentComment = models.ForeignKey('self', models.CASCADE, null=True, blank=True)