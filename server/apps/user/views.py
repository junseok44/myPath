from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from apps.user.models import User, UserCard
from apps.post.models import Post, BookMarkTable, LikeTable
import requests
import os
from django.http import JsonResponse
from urllib.parse import parse_qs
from json.decoder import JSONDecodeError

KAKAO_CLIENT_ID=os.environ.get("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URL="http://localhost:8000/user/kakaoRedirect"

GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URL = "http://localhost:8000/user/googleRedirect"

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
    
    ctx = {
        "KAKAO_CLIENT_ID":KAKAO_CLIENT_ID,
        "KAKAO_REDIRECT_URL":KAKAO_REDIRECT_URL,
    }
    return render(request, 'user/login.html', ctx)

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

def my_page(requests):

    if not requests.user.is_authenticated:
        return redirect("/")

    user_id = requests.user.id
    my_posts = Post.objects.filter(user=user_id).values()
    my_likes = LikeTable.objects.filter(user=user_id).select_related('post')
    my_bookmarks = BookMarkTable.objects.filter(user=user_id).select_related('post')
    user = User.objects.get(id=user_id)
    posts_count = Post.objects.filter(user=user_id).count()
    userCards = UserCard.objects.filter(writer=requests.user)

    ctx = {'my_posts': my_posts, 'my_likes': my_likes, 'my_bookmarks': my_bookmarks,'user': user, "posts_count":posts_count, "userCards": userCards}
    return render(requests, "user/my_page.html", ctx)

def user_page(requests, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user.id).values()
    posts_count = Post.objects.filter(user=user.id).count()

    ctx = {'user': user, 'posts': posts, 'posts_count': posts_count, "id": id} 
    return render(requests, "user/user_page.html", ctx)


def user_card_add(request):
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get("title")
        link = request.POST.get("link")
        desc = request.POST.get("desc")

        if len(title) > 10:
            messages.error(request,"소개는 10자 이내로 입력해주세요!")
            return redirect("/user/my_page")
        if len(title) > 100:
            messages.error(request,"설명은 100자 이내로 입력해주세요!")
            return redirect("/user/my_page")

        UserCard.objects.create(title=title,link=link,desc=desc, writer=request.user)
        messages.success(request, "유저카드를 추가했어요!")
        return redirect("/user/my_page")

    return redirect("/user/my_page")


def user_card_edit(request,id):
    card = get_object_or_404(UserCard, id=id)

    if request.method == "POST":
        title = request.POST.get("title")
        link = request.POST.get("link")
        desc = request.POST.get("desc")

        if len(title) > 10:
            messages.error(request, "제목은 10자 이내로 입력해주세요!")
            return redirect("/user/my_page")
        if len(desc) > 100:
            messages.error(request, "설명은 100자 이내로 입력해주세요!")
            return redirect("/user/my_page")

        card.title = title
        card.link = link
        card.desc = desc
        card.save()

        messages.success(request, "유저카드를 수정했어요!")
        return redirect("/user/my_page")

    return redirect("/user/my_page")

def user_card_delete(request, id):
    card = get_object_or_404(UserCard, id=id)

    if request.method == "POST":
        card.delete()
        messages.success(request, "유저카드를 삭제했어요!")
        return redirect("/user/my_page")

    return redirect("/user/my_page")

def user_intro_update(request):
    if request.method == 'POST':
        intro = request.POST.get('intro')
        print(intro)
        request.user.intro = intro
        request.user.save()
        return redirect('/user/my_page')  # Redirect to the same page after submission
    
    return redirect("/user/my_page")



def kakao_Auth_Redirect(request):
    code = request.GET.get('code', None)
    if code:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        content = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": KAKAO_REDIRECT_URL,
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
                    kakao_id = str(profile_data.get('id'))
                    user, created = User.objects.get_or_create(kakaoId=kakao_id)
                    if created:
                        user.username = username
                        user.loginId = kakao_id
                        user.password = kakao_id
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


def google_Auth_Start(request):
    scope = " https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid"
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URL}&scope={scope}")


# 현재 구글에서 닉네임이 안들어와서, 이메일의 일부를 수정했습니다.
def google_Auth_Redirect(request):
    code = request.GET.get("code")
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URL}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    profile_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    profile_req_status = profile_req.status_code
    if profile_req_status != 200:
        messages.error(request, "로그인에 실패했습니다! 다시 시도해주세요.")
        return redirect("/")
    profile_req_json = profile_req.json()
    userId = str(profile_req_json.get('user_id',''))
    if not userId:
        messages.error(request, "로그인에 실패했습니다! 다시 시도해주세요.")
        return redirect("/")
    email = profile_req_json['email']
    username = email.split("@")[0]
    if len(username) > 9:
        username = username[:9] + "@"  # Take the first 10 characters
    else:
        username = username + "@"
    hasUser = User.objects.filter(googleId=userId).exists()
    if not hasUser:
        user = User.objects.create(googleId=userId, username=username, loginId=userId, password=userId)
    user = User.objects.get(googleId=userId)
    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')        
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