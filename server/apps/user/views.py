from django.shortcuts import render

# Create your views here.



def view_user_main(requests):

    return render(requests, "user/main.html")