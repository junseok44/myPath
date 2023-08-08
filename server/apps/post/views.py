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

    if requests.user.is_authenticated:
        if LikeTable.objects.filter(post=post, user=requests.user).exists():
            post.isLiked = True
        else:
            post.isLiked = False
        
        if BookMarkTable.objects.filter(post=post, user=requests.user).exists():
            post.isBookMarked = True
        else:
            post.isBookMarked = False

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


def toggle_bookmark_ajax(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            user = request.user
            data = json.loads(request.body)
            post_id = data['postId']
            try:
                bookmark_entry = BookMarkTable.objects.get(user=user, post_id=post_id)
                bookmark_entry.delete()
                print("북마크 테이블 삭제")
                is_bookMarked = False
            except BookMarkTable.DoesNotExist:
                BookMarkTable.objects.create(user=user, post_id=post_id)
                print("북마크 테이블 추가")
                is_bookMarked = True
            targetPost = Post.objects.get(pk=post_id)
            count = BookMarkTable.objects.filter(post=targetPost).count()
            
            return JsonResponse({'isBookMarked': is_bookMarked, 'bookMark_count': count})
        except:
            return JsonResponse({"msg":"error"},status=404)

def toggle_like_ajax(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            user = request.user
            data = json.loads(request.body)
            post_id = data['postId']
            try:
                liketable_entry = LikeTable.objects.get(user=user, post_id=post_id)
                liketable_entry.delete()
                print("좋아요 테이블 삭제")
                is_Liked = False
            except LikeTable.DoesNotExist:
                LikeTable.objects.create(user=user, post_id=post_id)
                print("좋아요 테이블추가")
                is_Liked = True
            targetPost = Post.objects.get(pk=post_id)
            count = LikeTable.objects.filter(post=targetPost).count()
            return JsonResponse({'isLiked': is_Liked, 'like_count': count})
        except:
            return JsonResponse({"msg":"error"},status=404)
