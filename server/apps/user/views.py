from django.shortcuts import render
from apps.user.models import User
from apps.post.models import Post, BookMarkTable, LikeTable
from django.http import HttpResponse


def view_user_main(requests):

    return render(requests, "user/main.html")

def my_page(requests):
    user_id = requests.user.id
    my_posts = Post.objects.filter(user=user_id).values()
    my_likes = LikeTable.objects.filter(user=user_id).select_related('post')
    my_bookmarks = BookMarkTable.objects.filter(user=user_id).select_related('post')

    ctx = {'my_posts': my_posts, 'my_likes': my_likes, 'my_bookmarks': my_bookmarks}
    return render(requests, "user/my_page.html", ctx)

def user_page(requests, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user.id).values()
    posts_count = Post.objects.filter(user=user.id).count()

    ctx = {'user': user, 'posts': posts, 'posts_count': posts_count, "id": id} 
    return render(requests, "user/user_page.html", ctx)

