from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',view_post_main,name='post_main'),
    path('post/list', view_post_list, name="post_list"),
    path('post/<uuid:pk>',view_post_detail,name='post_detail'),
    path('post/step',view_step_detail_ajax,name='step_detail'),
    path('post/step/create_comment',view_step_create_comment_ajax,name='step_create_comment'),
    path('post/<uuid:pk>/create_comment',view_post_create_comment,name='post_create_comment'),
    path('api/toggleBookMark/', toggle_bookmark_ajax),
    path('api/toggleLike/', toggle_like_ajax)   ,

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)