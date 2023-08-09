from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',view_post_main,name='post_main'),
    path('post/list', view_post_list, name="post_list"),
    path('post/<uuid:pk>',view_post_detail,name='post_detail'),
    path('post/<uuid:pk>/comment_create',view_post_detail,name='post_comment_create'),
    path('post/step',view_step_detail_ajax,name='step_detail'),
    path('post/step/comment_create',view_step_comment_create_ajax,name='step_comment_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)