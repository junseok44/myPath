from django.shortcuts import render
from apps.user.models import User
from apps.post.models import Post, BookMarkTable, LikeTable
from django.http import HttpResponse


def view_user_main(requests):

    return render(requests, "user/main.html")

def my_page(requests):
    my_posts = Post.objects.all()
    bookmark_posts = BookMarkTable.objects.all()
    like_posts = LikeTable.objects.all()

    ctx = {'my_posts': my_posts, 'bookmark_posts': bookmark_posts, 'like_posts': like_posts}
    return render(requests, "user/my_page.html", ctx)

def user_page(requests, id):
    user = User.objects.get(id=id)
    posts = Post.objects.all()

    ctx = {'user': user, 'posts': posts, "id": id} 
    return render(requests, "user/user_page.html", ctx)

