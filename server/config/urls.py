
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('apps.user.urls')),
    # path('chat/',include('apps.chatting.urls')),
    path('',include('apps.post.urls')),
]
