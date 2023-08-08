from django.shortcuts import render
from apps.post.models import *
from apps.comment.models import PostComment,StepComment

# Create your views here.

def view_post_main(requests):
    return render(requests, "post/main.html")

def view_post_detail(requests,pk):

    post=Post.objects.get(id=pk)
    paths=Path.objects.filter(post=post).order_by("order")
    for path in paths:
        path.steps=Step.objects.filter(path=path).order_by("order") #?
    post_comments=PostComment.objects.filter(post=post)
    ctx={"post":post,"paths":paths,"post_comments":post_comments}

    return render(requests,"post/detail.html",context=ctx)