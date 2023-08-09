from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages

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