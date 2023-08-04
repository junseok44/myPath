from django.shortcuts import render

# Create your views here.

def view_post_main(requests):
    return render(requests, "post/main.html")