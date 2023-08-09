from django.shortcuts import render,get_object_or_404,redirect
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

def view_post_comment_create(request,pk):
    if request.method=="POST":
        comment = PostComment() 
        comment.post=Post.objects.get(id=pk)
        comment.text = request.POST['comment']
        comment.save()
        
    return redirect(f'/post/{pk}/')  



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

@csrf_exempt
def view_step_detail_ajax(request):
    req=json.loads(request.body)
    step_id=req['id']
    step=get_object_or_404(Step, pk=step_id)
    step_comments=StepComment.objects.filter(step=step)
    step_json=serialize('json',step)
    step_comments_json=serialize('json',step_comments)
    step_json=serialize('json',step)
    step_comments_json=serialize('json',step_comments_json)
    ctx={"step":step_json,"step_comments":step_comments_json}

    return JsonResponse(ctx)

@csrf_exempt
def view_step_comment_create_ajax(request):
    req=json.loads(request.body)
    step_id=req['id']
    content=req['content']
    if request.method=="POST":
        step=Step.objects.get(id=step_id)
        comment=StepComment.objects.create(
            step=step,
            text=content,
        )
        # comment.save()
    ctx={'id':step_id,'comment_id':comment.id,'content':content}
    return JsonResponse(ctx)
    