from django.contrib.auth import get_user_model
from django.db import models
import uuid
# from apps.user.models import User

User = get_user_model()

class Post(models.Model):
    pathMode = [
        ('col', '세로모드'),
        ('row', '가로모드')
    ]
    user = models.ForeignKey(User, models.CASCADE, related_name='post')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,  editable=False)
    title = models.CharField(max_length=20, blank=False, null=False)
    desc = models.CharField(max_length=500, blank=False, null=False)
    mode = models.CharField(max_length=5,
                            choices=pathMode, default="col", blank=False, null=False)
    review = models.CharField(max_length=500, blank=True, default='')
    thumbnail = models.ImageField(upload_to="post/", blank=True, null=True)

    def __str__(self):
        return self.title

class Path(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('Post', models.CASCADE, related_name="path")
    title = models.CharField(max_length=10, blank=True, default='')
    order = models.IntegerField()


class Step(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    path = models.ForeignKey(Path, models.CASCADE, related_name="step")
    title = models.CharField(max_length=20, blank=False, null=False)
    desc = models.CharField(max_length=500, blank=False, null=False)
    order = models.IntegerField()
    Image = models.ImageField(upload_to="step/", blank=True, null=True)



class Category(models.Model):
    name = models.CharField(max_length=10)

class CategoryTable(models.Model):
    post = models.ForeignKey('Post', models.CASCADE, related_name="category_table")
    category = models.ForeignKey(Category, models.CASCADE, related_name="category_table")
    

class Tag(models.Model):
    name = models.CharField(max_length=10)

class TagTable(models.Model):
    post = models.ForeignKey('Post', models.CASCADE, related_name="tag_table")
    tag = models.ForeignKey(Tag,models.CASCADE, related_name="tag_table")



class Curation(models.Model):
    name = models.CharField(max_length=20)

class CurationTable(models.Model):
    curation = models.ForeignKey(Curation, models.CASCADE, related_name="curation_table")
    post = models.ForeignKey('Post', models.CASCADE, related_name="curation_table")


class BookMarkTable(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="bookmark_table")
    user = models.ForeignKey(User, models.CASCADE, related_name="bookmark_table")

class LikeTable(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="like_table")
    user = models.ForeignKey(User, models.CASCADE, related_name="like_table")



