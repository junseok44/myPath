from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',view_post_main,name='post_main'),
    path('post/list', view_post_list, name="post_list"),
    path('post/<uuid:pk>',view_post_detail,name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)