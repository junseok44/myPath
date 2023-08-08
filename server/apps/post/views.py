from django.shortcuts import render
from apps.post.models import *
from apps.comment.models import PostComment,StepComment

# Create your views here.

def view_post_main(requests):
    return render(requests, "post/main.html")

def view_post_list(requests):
    posts=Post.objects.all()
    ctx={"posts":posts}
    return render(requests,"post/post_list.html",context=ctx)

def view_post_detail(requests,pk):

    post=Post.objects.get(id=pk)
    paths=Path.objects.filter(post=post).order_by("order")
    for path in paths:
        path.steps=Step.objects.filter(path=path).order_by("order") #?
    post_comments=PostComment.objects.filter(post=post)
    ctx={"post":post,"paths":paths,"post_comments":post_comments}

    return render(requests,"post/detail.html",context=ctx)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view_step_detail_ajax(request):
    req=json.loads(request.body)
    step_id=req['id']
    step=Step.objects.get(id=step_id)

    return JsonResponse()

@csrf_exempt
def view_step_comment_create_ajax(request):
    req=json.loads(request.body)
    step_id=req['id']
    step=Step.objects.get(id=step_id)
    
    return JsonResponse()
