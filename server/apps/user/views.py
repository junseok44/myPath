from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages
from apps.user.models import User
from apps.post.models import Post, BookMarkTable, LikeTable

def user_main(request):  
    return render(request, 'user/login.html')

def user_login(request):  
    if request.method == "POST":
        login_id = request.POST.get('loginId')
        password = request.POST.get('password')
        user = authenticate(request, username=login_id, password=password)
        
        if user is not None:
            auth_login(request, user) 
            messages.success(request, "성공적인 로그인입니다!")
            return redirect('user_main')
        else:
            messages.error(request, "실패한 로그인입니다!")
            return render(request, 'user/login.html', {'error': 'Invalid credentials.'})
    
    return render(request, 'user/login.html')

def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  
            messages.success(request, "성공적인 회원가입 & 로그인입니다!")
            return redirect('user_main')
        else:
            messages.error(request, "회원가입에 실패하였습니다.")
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})



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

