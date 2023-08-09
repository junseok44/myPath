from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm

def user_main(request):  
    return render(request, 'user/login.html')

def user_login(request):  
    if request.method == "POST":
        login_id = request.POST.get('loginId')
        password = request.POST.get('password')
        user = authenticate(request, username=login_id, password=password)
        
        if user is not None:
            auth_login(request, user) 
            return redirect('user_main')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials.'})
    
    return render(request, 'user/login.html')

def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  
            return redirect('user_main')
        else:
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})