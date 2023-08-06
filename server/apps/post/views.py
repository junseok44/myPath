from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Post, Path, Step, Category, CategoryTable
from django.core.serializers import serialize

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
        if not request.user.is_authenticated:
            user = get_user_by_username("개미개미")
        else:
            user = request.user
        print(user.get_username())
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

        print(data['category'])
        cat = Category.objects.get(name=data['category'])
        CategoryTable.objects.create(
            post=post,
            category=cat
        )

        for path in data['paths']:
            newPath = Path.objects.create(
                post=post,
                title=path['title'],
                order=path['order']
            )
            print("path 생성", newPath)
            for step in [step for step in data['steps'] if step['pathId'] == path['id']]:
                Image_data = step.get("Image")
                if Image_data is not None:
                    newStep = Step.objects.create(
                        path=newPath,
                        title=step['title'],
                        desc=step['desc'],
                        order=step['order'],
                        Image=step['Image']
                    )
                else:
                    newStep = Step.objects.create(
                        path=newPath,
                        title=step['title'],
                        desc=step['desc'],
                        order=step['order'],
                    )
                print("step생성", newStep)

        return JsonResponse({"msg": "hello"})

    categories = Category.objects.all()
    return render(request, "post/post_write.html",
                  
                  {"categories": categories})


def view_post_list(request):
    posts = Post.objects.all()
    ctx = {
        "posts": posts
    }

    return render(request, 'post/post_list.html', ctx)


def view_post_edit(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = get_object_or_404(Post, pk=id)

        # 1. 삭제된 id를 삭제한다.
        for deletedId in data['deletedPaths']:
            matching_objects = Path.objects.filter(pk=deletedId)
            if matching_objects.exists():
                for obj in matching_objects:
                    print("deleted columns"+obj.title)
                    obj.delete()


        for deletedId in data['deletedIds']:
            matching_objects = Step.objects.filter(pk=deletedId)
            if matching_objects.exists():
                for obj in matching_objects:
                    print("deleted steps"+obj.title)
                    obj.delete()

        # 1. Create 기존 컬럼에 추가된 스텝을 추가한다.
        for item in [data for data in data['steps'] if data['isNew'] == True]:
            matching_objects = Path.objects.filter(pk=item['pathId'])
            if matching_objects.exists():
                step = Step.objects.create(
                    path=Path.objects.get(pk=item['pathId']),
                    title=item['title'],
                    desc=item['desc'],
                    order=item['order'],
                )
                print("created into current path", step.title)

        # 2. Create 새로운 컬럼을 추가하고, 그 컬럼에 해당하는 step도 추가한다.
        for path in [path for path in data['paths'] if path['isNew'] == True]:
            newPath = Path.objects.create(
                post=post, title=path['title'], order=path['order'])
            for step in [step for step in data['steps'] if step['pathId'] == path['id']]:
                newStep = Step.objects.create(path=newPath, title=step['title'], desc=step['desc'],
                                              order=step['order']
                                              )
                print("created new step in new column", newStep.title)

        # 기존 path 중에서 수정된것을 반영한다.
        for path in [path for path in data['paths'] if path['isEdited'] == True and path['isNew'] == False]:
            matching_objects = Path.objects.filter(pk=path['id'])
            if matching_objects.exists():
                for obj in matching_objects:
                    obj.title = path['title']
                    obj.order = path['order']


        # 3. Update 그 다음 편집되었던 step을 골라서. 해당 실제 데이터로 넣어준다. title,desc,order 등.
        for step in [step for step in data['steps'] if step['isEdited'] == True and step['isNew'] == False]:
            myStep = get_object_or_404(Step, pk=step['id'])
            myStep.title = step['title']
            myStep.desc = step['desc']
            myStep.order = step['order']
            myStep.save()
            print("edited step", myStep.title)

        post.title = data['title']
        post.desc = data['desc']
        post.review = data['review']
        
        category = Category.objects.get(name=data['category'])
        table = CategoryTable.objects.get(post=post)
        table.category = category
        table.save()
        post.save()

        return JsonResponse({"msg": "hello"})

    post = get_object_or_404(Post, id=id)
    paths = Path.objects.filter(post=post)
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
