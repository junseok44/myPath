from django.shortcuts import render
from .models import Post, Path, Step
# from apps.user.models import User
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
import json

User = get_user_model()
# Create your views here.


def view_post_main(requests):
    return render(requests, "post/main.html")


def get_user_by_username(username):
    try:
        print("find user")
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        print("create new user")
        newUser = User.objects.create_user(
            username=username, loginId="myOne", password='jang1234', intro='Test intro')
        return newUser


def view_post_write(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # if not request.user.is_authenticated:
        user = get_user_by_username("개미개미")
        print(user.get_username())

        # post = Post.objects.create(
        #     user=user,
        #     title=data['title'],
        #     desc=data['desc'],
        # )
        # print("post 생성", post)
        # for path in data['paths']:
        #     newPath = Path.objects.create(
        #         post=post,
        #         title=path['title'],
        #         order=path['order']
        #     )
        #     print("path 생성", newPath)
        #     for step in [step for step in data['steps'] if step['pathId'] == path['id']]:
        #         Image_data = step.get("Image")
        #         if Image_data is not None:
        #             newStep = Step.objects.create(
        #                 path=path,
        #                 title=step['title'],
        #                 desc=step['desc'],
        #                 order=step['order'],
        #                 Image=step['Image']
        #             )
        #         else:
        #             newStep = Step.objects.create(
        #                 path=path,
        #                 title=step['title'],
        #                 desc=step['desc'],
        #                 order=step['order'],
        #             )
        #         print("step생성", newStep)

        return JsonResponse({"msg": "hello"})

    return render(request, "post/post_write.html")


def view_post_list(request):
    posts = Post.objects.all()
    ctx = {
        "posts": posts
    }

    return render(request, 'post/post_list.html', ctx)


def view_post_edit(request):
    return render(request, 'post/post_edit.html')
