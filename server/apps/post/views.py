from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import *
from apps.comment.models import *
from django.core.serializers import serialize
from django.contrib import messages 
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, CategoryTable

import base64
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Q

User = get_user_model()
# Create your views here.


def view_post_main(requests): 
        categories = Category.objects.all()
        allcuration__list = []
        curation__ids = [1,2]
        for cur__id in curation__ids:
                try:
                        curation = Curation.objects.get(pk=cur__id)
                        curation__tables = CurationTable.objects.filter(curation=curation)
                        curation__list = []
                        for table in curation__tables:
                            curation__list.append(table.post)
                        allcuration__list.append({"name": curation.name, "list": curation__list})
                except:
                        continue

        ctx = {
               "categories": categories,
               "curations": allcuration__list
        }
   
        return render(requests, "post/main.html",ctx)


def category_search(request, category_id):
    category = Category.objects.get(id=category_id)
    category_tables = CategoryTable.objects.filter(category=category)
    categories = Category.objects.all()
    category_posts = []

    for tables in category_tables:
           category_posts.append(tables.post)

    items_per_page = 6  
    paginator = Paginator(category_posts, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    ctx = {
            "category_name": category.name,
            "category": category,
            "category_posts": category_posts,
            "categories": categories,
            "page":page,
            "current_category_id": category_id,
    }
    return render(
        request,
        "post/main__category.html",
        ctx
    )

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

def get_image_from_dataUrl(dataUrl):
    image_data = None 
    if dataUrl:
        format, imgstr = dataUrl.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')

    return image_data

@transaction.atomic
@login_required(login_url="/user/login")
def view_post_write(request):
    if request.method == "POST":
        try:
            data = {}
            data['thumbnail'] = request.FILES.get("thumbnail")
            data['paths'] = json.loads(request.POST.get("paths"))
            data['steps'] = json.loads(request.POST.get("steps"))
            data['title'] = request.POST.get("title")
            data['desc'] = request.POST.get("desc")
            data['review'] = request.POST.get("review")
            data['tags'] = json.loads(request.POST.get("tags"))
            data['category'] = request.POST.get("category")
            data['mode'] = request.POST.get("mode")

            if not request.user.is_authenticated:
                messages.error(request, '글을 쓰시려면 로그인해야해요!')
                return JsonResponse({"error": "errormessage"}, status=500) 
            else:
                user = request.user

            #썸네일 있는지 확인후, post 생성.
            thumbnail_data = data.get("thumbnail")
            if thumbnail_data is not None:
                post = Post.objects.create(
                    user=user,
                    title=data['title'],
                    desc=data['desc'],
                    review=data['review'],
                    mode=data['mode'],
                    thumbnail=data['thumbnail']
                )
            else:
                post = Post.objects.create(
                    user=user,
                    title=data['title'],
                    desc=data['desc'],
                    review=data['review'],
                    mode=data['mode'],
                )
            print("post 생성", post)

            #카테고리 불러온후, post와 연결
            cat = Category.objects.get(name=data['category'])
            CategoryTable.objects.create(
                post=post,
                category=cat
            )
            
            #태그 불러온후, 없으면 생성후 연결, 있으면 연결
            for tagName in data['tags']:
                tagObj = Tag.objects.filter(name=tagName)
                if tagObj.exists():
                    for tag in tagObj:
                        #하나의 tag 인스턴스임.
                        tagtable = TagTable.objects.create(
                            post=post,
                            tag=tag
                        )
                        print("tagable 연결", tagtable.tag.name)
                else:
                    newTag = Tag.objects.create(name=tagName)
                    print("태그생성",newTag.name)
                    tagtable = TagTable.objects.create(
                            post=post,
                            tag=newTag
                        )
                    print("tagable 연결", tagtable.tag.name)

            #새로운 패스와 거기에 해당하는 스텝 생성.
            for path in data['paths']:
                newPath = Path.objects.create(
                    post=post,
                    title=path['title'],
                    order=path['order']
                )
                print("path 생성", newPath)
                for step in [step for step in data['steps'] if step['pathId'] == path['id']]:
                    Image_url = step.get("image")
                    Image_data = get_image_from_dataUrl(Image_url)
                    if Image_data is not None:
                        newStep = Step.objects.create(
                            path=newPath,
                            title=step['title'],
                            desc=step['desc'],
                            order=step['order'],
                            Image=Image_data
                        )
                    else:
                        newStep = Step.objects.create(
                            path=newPath,
                            title=step['title'],
                            desc=step['desc'],
                            order=step['order'],
                        )
                    print("step생성", newStep)

            messages.success(request, '패스를 생성했습니다!')
            return JsonResponse({"id": post.id})
        except Exception as e:
            print(e)
            messages.error(request, '작성에 실패했습니다! 다시 시도해주세요')
            return JsonResponse({"error": "errormessage"}, status=500)  # Internal Server Error

    categories = Category.objects.all()
    return render(request, "post/post_write.html",
                  {"categories": categories})

def view_post_list(request):
    posts = Post.objects.all()
    ctx = {
        "posts": posts
    }
    return render(request, 'post/post_list.html', ctx)

def view_post_delete(request, id):
    try:
        print("삭제")
        print(id)
        deletedPost = Post.objects.get(pk=id)
        deletedPost.delete()
        messages.success(request, '성공적으로 삭제되었습니다.')
        return JsonResponse({"msg":"success"},status = 200)
    except:
        messages.error(request, 'delete failed')
        return JsonResponse({"msg":"error"},status = 404)

@transaction.atomic
@login_required(login_url="/user/login")
def view_post_edit(request, id):

    if request.method == "POST":
        try:
            data = {}
            data['thumbnail'] = request.FILES.get("thumbnail")
            data['paths'] = json.loads(request.POST.get("paths"))
            data['steps'] = json.loads(request.POST.get("steps"))

            data['deletedPaths'] = json.loads(request.POST.get('deletedPaths'))
            data['deletedIds'] = json.loads(request.POST.get('deletedIds'))
            data['title'] = request.POST.get("title")
            data['desc'] = request.POST.get("desc")
            data['review'] = request.POST.get("review")
            data['category'] = request.POST.get("category")

            data['deletedTag'] = json.loads(request.POST.get("deletedTag"))
            data['addedTag'] = json.loads(request.POST.get("addedTag"))
            data['mode'] = request.POST.get("mode")

            # data = json.loads(request.body)
            post = get_object_or_404(Post, pk=id)
            print(post)
            # 1. 삭제된 path를 삭제한다.
            for deletedId in data['deletedPaths']:
                matching_objects = Path.objects.filter(pk=deletedId)
                if matching_objects.exists():
                    for obj in matching_objects:
                        print("deleted columns"+obj.title)
                        obj.delete()

            # 삭제된 step을 삭제한다.
            for deletedId in data['deletedIds']:
                matching_objects = Step.objects.filter(pk=deletedId)
                if matching_objects.exists():
                    for obj in matching_objects:
                        print("deleted steps"+obj.title)
                        obj.delete()

            # 1. Create 기존 패스에 추가된 스텝을 추가한다.
            for step in [data for data in data['steps'] if data['isNew'] == True]:
                matching_objects = Path.objects.filter(pk=step['pathId'])
                if matching_objects.exists():
                    if step.get('image') != None and step.get('image') != "":
                           step = Step.objects.create(
                            path=Path.objects.get(pk=step['pathId']),
                            title=step['title'],
                            desc=step['desc'],
                            order=step['order'],
                            Image=get_image_from_dataUrl(step['image'])
                        )
                    else:    
                        step = Step.objects.create(
                            path=Path.objects.get(pk=step['pathId']),
                            title=step['title'],
                            desc=step['desc'],
                            order=step['order'],
                        )
                    print("created into current path", step.title)

            # 2. Create 새로운 패스를 추가하고, 그 패스에 해당하는 step도 추가한다.
            for path in [path for path in data['paths'] if path['isNew'] == True]:
                print(path["id"])
                newPath = Path.objects.create(
                    post=post, title=path['title'], order=path['order'])
                for step in [step for step in data['steps'] if step['pathId'] == path['id']]:
                    if step.get('image') != None and step.get('image') != "":
                        newStep = Step.objects.create(path=newPath, title=step['title'], desc=step['desc'],
                                                  order=step['order'], Image=get_image_from_dataUrl(step['image'])
                                                  )
                    else:
                        newStep = Step.objects.create(path=newPath, title=step['title'], desc=step['desc'],
                                                  order=step['order']
                                                  )
                    print("created new step in new column", newStep.title)


            #update
            # 기존 path 중에서 수정된것을 반영한다.
            for path in [path for path in data['paths'] if path['isEdited'] == True and path['isNew'] == False]:
                print(path)
                matching_objects = Path.objects.filter(pk=path['id'])
                if matching_objects.exists():
                    for obj in matching_objects:
                        print(obj)
                        obj.title = path['title']
                        obj.order = path['order']
                        obj.save()


            # 3. Update 그 다음 편집되었던 step을 골라서. 해당 실제 데이터로 넣어준다. title,desc,order 등.
            for step in [step for step in data['steps'] if step['isEdited'] == True and step['isNew'] == False]:
                myStep = get_object_or_404(Step, pk=step['id'])
                myStep.title = step['title']
                myStep.desc = step['desc']
                myStep.order = step['order']
                if step.get('image') != None and step.get('image') != "":
                    myStep.Image = get_image_from_dataUrl(step['image'])
                myStep.save()
                print("edited step", myStep.title)

            # post를 수정한다.
            post.title = data['title']
            post.desc = data['desc']
            post.review = data['review']
            if data.get('thumbnail'):
                post.thumbnail = data.get('thumbnail')

            # post category 수정
            category = Category.objects.get(name=data['category'])
            table = CategoryTable.objects.get(post=post)
            table.category = category
            table.save()
            post.save()

            # post tag 삭제.
            for dTagName in data['deletedTag']:
                try:
                    print(dTagName)
                    dTag = Tag.objects.get(name=dTagName)
                    dTagTable = TagTable.objects.get(tag=dTag, post=post)
                    print(dTagTable)
                    dTagTable.delete()
                except:
                    pass
                
            # post tag 추가.
            for tagName in data['addedTag']:
                tagObj = Tag.objects.filter(name=tagName)
                if tagObj.exists():
                    for tag in tagObj:
                        tagtable = TagTable.objects.create(
                            post=post,
                            tag=tag
                        )
                        print("tagable 연결", tagtable.tag.name)
                else:
                    newTag = Tag.objects.create(name=tagName)
                    print("태그생성",newTag.name)
                    tagtable = TagTable.objects.create(
                            post=post,
                            tag=newTag
                        )
                    print("tagable 연결", tagtable.tag.name)

            messages.success(request, "성공적으로 수정했습니다!!")
            return JsonResponse({"msg": "hello"})

        except Exception as e:
            print(e)
            messages.error(request, "수정에 실패했습니다. 다시 시도해주세요!")
            return JsonResponse({"error":"an error occurred"},status=404)

    post = get_object_or_404(Post, id=id)
    paths = Path.objects.filter(post=post).order_by("order")

    for path in paths:
        path.steps = path.step.all().order_by("order")

    jsonPost = serialize('json', [post])
    jsonPaths = serialize('json', paths)
    jsonSteps = serialize('json', Step.objects.filter(path__in=paths))
    currentCategory = CategoryTable.objects.get(post=post).category.name
    categories = Category.objects.all()
    ctx = {
        "post": post,
        "paths": paths,
        "jsonPost": jsonPost,
        "jsonPaths": jsonPaths,
        "jsonSteps": jsonSteps,
        "currentCategory":currentCategory,
        "categories": categories,
    }

    return render(request, 'post/post_edit.html', ctx)


def view_post_detail(requests,pk):

    post=Post.objects.get(id=pk)
    post_category = CategoryTable.objects.get(post=post).category.name
    post_category_id = CategoryTable.objects.get(post=post).category.id
    post_tags=TagTable.objects.filter(post=post)
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

    ctx={
            "post":post,
            "post_category":post_category,
            "post_category_id": post_category_id,
            "post_tags":post_tags,
            "paths":paths,
            "post_comments":post_comments
        }

    return render(requests,"post/detail.html",context=ctx)

def view_post_create_comment(request,pk):
    if request.method=="POST": 
        if request.user.is_authenticated:
            if request.POST['comment'] == "":
                messages.error(request, "공백은 입력하실수 없습니다.")
                return redirect(f'/post/{pk}')

            parentId = request.POST.get("parentCommentId")
            if parentId is not None:
                print(parentId)
                parentComment = get_object_or_404(PostComment,pk=parentId)
                print(parentComment)
                PostComment.objects.create(
                writer=request.user,
                post=Post.objects.get(id=pk),
                text = request.POST['comment'],
                parentComment=parentComment)
            else:
                PostComment.objects.create(
                writer=request.user,
                post=Post.objects.get(id=pk),
                text = request.POST['comment']
            )
            return redirect(f'/post/{pk}')
        else:
            messages.error(request, "댓글 작성을 위해서 로그인해주세요!")
            return redirect(f'/post/{pk}')

    return render(request,"post/detail.html")

def view_post_delete_comment_ajax(request):
    req=json.loads(request.body)
    post_id=req['post_id']
    comment_id=req['comment_id']
    post=Post.objects.get(id=post_id)
    comment=PostComment.objects.get(post=post, id=comment_id)
    if request.method=="POST" and request.user.is_authenticated:
        print(comment, request.user, comment.writer)
        if(request.user==comment.writer):
            comment_json=serialize('json', [comment])
            comment.delete()
            return JsonResponse({'comment':comment_json})
    else:
        return HttpResponse('Failed: Post requests only.')

def view_step_detail_ajax(request):
    req = json.loads(request.body)
    step_id = req['step_id']

    if request.method=="POST":
        step = get_object_or_404(Step, pk=step_id)
        user=request.user.username
        step_comments = StepComment.objects.filter(step=step)
        step_list = [
            {"fields":{
                "step": str(comment.step.id),
                "text":comment.text,
                "writer":comment.writer.username
            }, "pk": comment.pk} for comment in step_comments
        ]
        step_json = serialize('json', [step])
        # step_comments_json = serialize('json', step_list)
        step_comments_json = json.dumps(step_list)
        ctx = {"user":user,"step": step_json, "step_comments": step_comments_json, }

        return JsonResponse(ctx)
    else:
        return HttpResponse('Failed: Post requests only.')
    
def view_step_create_comment_ajax(request):
    req=json.loads(request.body)
    step_id=req['step_id']
    text=req['text']
    if request.method=="POST":
        if request.user.is_authenticated:
            if text == "":
                messages.error(request, "공백은 입력하실수 없습니다.")
                return JsonResponse({"error": "errormessage"}, status=500)
            else:
                comment=StepComment.objects.create(
                    writer=request.user,
                    step=get_object_or_404(Step, pk=step_id),
                    text=text,
                )
                ctx={'step_id':step_id,'comment_id':comment.id,'writer':comment.writer.username,'text':text}
                return JsonResponse(ctx)
        else:
            messages.error(request,"댓글 작성을 위해 로그인해주세요!")
            return JsonResponse({},status=400)
    else:
        return HttpResponse('Failed: Post requests only.')

def view_step_delete_comment_ajax(request):
    req=json.loads(request.body)
    step_id=req['step_id']
    comment_id=req['comment_id']
    step=Step.objects.get(id=step_id)
    comment=StepComment.objects.get(step=step, id=comment_id)
    

    if request.method=="POST" and request.user.is_authenticated:
        if(request.user==comment.writer):
            comment_json=serialize('json', [comment])
            comment.delete()
            return JsonResponse({'comment':comment_json})
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

def search(request):
        post_list = Post.objects.all()
        categories=Category.objects.all()
        # page=request.GET.get('page')

        # paginator = Paginator(post_list, 6)

        # try:
        #     page_obj = paginator.page(page) 
        # except PageNotAnInteger:
        #     page =1
        #     page_obj = paginator.page(page)
        # except EmptyPage:
        #     page = paginator.num_pages
        #     page_obj = paginator.page(page)

                        
        if request.method == 'POST':
                searched = request.POST['searched']        
                searched_posts = Post.objects.filter(title__contains=searched)
                return render(request, 'post/searched.html', {'searched': searched, 'searched_posts': searched_posts,'categories':categories})
        else:
                return render(request, 'post/searched.html', {'categories':categories,})
        
def search_by_category(request, id):
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    category_tables = CategoryTable.objects.filter(category=category)
    category_posts = [table.post for table in category_tables]

    if request.method == 'POST':
        searched = request.POST.get('searched')
        
        # Filter posts within the category
        searched_posts = Post.objects.filter(
            Q(id__in=[post.id for post in category_posts]) &
            Q(title__icontains=searched)
        )
        
        return render(request, 'post/search_by_category.html', {
            'searched': searched,
            'searched_posts': searched_posts,
            'category_name': category.name,
            'category': category,
            'categories':categories,
        })
    else:
        return render(request, 'post/search_by_category.html', {
            'category_name': category.name,
            'category': category,
            'categories':categories,
        })






def index(request):
    page = request.GET.get('page', '1')  # 페이지
    page_post_list = Post.objects.order_by('-create_date')
    paginator = Paginator(page_post_list, 6)  # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

# views.py

from django.core.mail import send_mail
from django.conf import settings

def report_post(request,pk):
    
    if request.method == 'POST':
        # reason = request.POST.get('reason')
        user = request.user
        data = json.loads(request.body)
        post_id=data['post_id']
        url=data['url']
        post=get_object_or_404(Post,id=pk)
        
        # Send email to the admin
        subject = f"Report for Post: {post.title}"
        message=f"user {user}가 신고한 포스트입니다:{url}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['stabthecake0044@gmail.com']
        
        send_mail(subject, message, from_email, recipient_list) 
        return JsonResponse({"msg":"success"})

    else:
        return JsonResponse({"error": "errormessage"}, status=404) 
