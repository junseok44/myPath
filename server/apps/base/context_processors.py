from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.post.models import Push


def get_push_list(request):

    if not request.user.is_authenticated:
        return {}
    else:
        push_list = Push.objects.filter(receiver=request.user).order_by('-created_at')[:5]
        unread_count = Push.objects.filter(receiver=request.user, is_read=False).count()
        ctx = {
        'push_list': push_list,
        "unread_count" :unread_count,
    }
  
    return ctx

