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

def view_post_create_comment(request,pk):
    if request.method=="POST":
        comment = PostComment() 
        comment.post=Post.objects.get(id=pk)
        comment.text = request.POST['comment']
        comment.save()
        
    return redirect(f'/post/{pk}/')  



import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize


@csrf_exempt
def view_step_detail_ajax(request):
    req = json.loads(request.body)
    step_id = req['step_id']

    if request.method=="POST":
        step = get_object_or_404(Step, pk=step_id)
        step_comments = StepComment.objects.filter(step=step)

        step_json = serialize('json', [step])
        step_comments_json = serialize('json', step_comments)

        ctx = {"step": step_json, "step_comments": step_comments_json}

        return JsonResponse(ctx)
    else:
        return HttpResponse('Failed: Post requests only.')
    
@csrf_exempt
def view_step_create_comment_ajax(request):
    req=json.loads(request.body)
    step_id=req['step_id']
    text=req['text']
    if request.method=="POST":
        comment=StepComment.objects.create(
            writer=request.user,
            step=get_object_or_404(Step, pk=step_id),
            text=text,
        )
        ctx={'step_id':step_id,'comment_id':comment.id,'text':text}
        return JsonResponse(ctx)
    else:
        return HttpResponse('Failed: Post requests only.')


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
