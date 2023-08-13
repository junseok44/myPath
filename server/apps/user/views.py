from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from apps.user.models import User
from apps.post.models import Post, BookMarkTable, LikeTable
# import requests

def user_main(request):  
    return render(request, 'user/login.html')

def user_login(request):  
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        login_id = request.POST.get('loginId')
        password = request.POST.get('password')
        user = authenticate(request, loginId=login_id, password=password)
        
        if user is not None:
            auth_login(request, user) 
            messages.success(request, "성공적인 로그인입니다!")
            return redirect('/')
        else:
            messages.error(request, "실패한 로그인입니다!")
            return render(request, 'user/login.html', {'error': 'Invalid credentials.'})
    
    return render(request, 'user/login.html')

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='apps.user.backends.LoginIDBackend') 
            messages.success(request, "성공적인 회원가입 & 로그인입니다!")
            return redirect('/')
        else:
            messages.error(request, "회원가입에 실패하였습니다.")
            return render(request, 'user/signup.html', {'form': form})
        
    else:
        form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("/")


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

def kakao_Auth_Redirect(request):
    code = request.GET.get('code', None)
    if code:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        content = {
            "grant_type": "authorization_code",
            "client_id": " ",
            "redirect_uri": " ",
            "code": code,
        }
        token_res = requests.post("https://kauth.kakao.com/oauth/token", headers=headers, data=content)

        if token_res.status_code == 200:
            token_data = token_res.json()
            access_token = token_data.get('access_token')

            headers123 = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            }
            profile_res = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers123)

            if profile_res.status_code == 200:
                profile_data = profile_res.json()
                properties = profile_data.get('properties')
                if properties and 'nickname' in properties:
                    username = properties['nickname']
                    kakao_id = profile_data.get('id')

                    user, created = User.objects.get_or_create(kakaoId=kakao_id)
                    if created:
                        user.username = username
                        user.save()

                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
                else:
                    print("Kakao API에서 닉네임 정보를 가져오지 못했습니다.")
            else:
                print("Kakao API에서 프로필 정보를 가져오지 못했습니다.")
        else:
            print("Kakao API에서 토큰 발급에 실패했습니다.")

    return redirect("/")



def naver_Auth_Redirect(request):
    code = request.GET.get('code', None)
    if code:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        content = {
            "grant_type": "authorization_code",
            "client_id": " ",  
            "client_secret": " T", 
            "redirect_uri": "http://localhost:8000/user/naverRedirect",  
            "code": code,
        }
        token_res = requests.post("https://nid.naver.com/oauth2.0/token", headers=headers, data=content)

        if token_res.status_code == 200:
            token_data = token_res.json()
            access_token = token_data.get('access_token')

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            profile_res = requests.get("https://openapi.naver.com/v1/nid/me", headers=headers)

            if profile_res.status_code == 200:
                profile_data = profile_res.json()
                response_data = profile_data.get('response')
                if response_data:
                    username = response_data['nickname']
                    naver_id = response_data['id']

                    # 모델에 naverId ,, 이건 냅둘게 모델이라
                    user, created = User.objects.get_or_create(naverId=naver_id)
                    if created:
                        user.username = username
                        user.save()

                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
                else:
                    messages.error(request, "네이버 프로필 정보를 가져오지 못했습니다.")
            else:
                messages.error(request, "네이버 프로필 정보 요청에 실패하였습니다.")
        else:
            messages.error(request, "네이버 토큰 발급에 실패하였습니다.")

    return redirect("/")