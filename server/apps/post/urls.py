from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', view_post_main, name='post_main'),
    path('post/write', view_post_write, name="post_write"),
    path('post/edit/<uuid:id>', view_post_edit, name="post_edit"),
    path('post/delete/<uuid:id>', view_post_delete, name="post_delete"),
    path('post/list', view_post_list, name="post_list"),
    path('post/<uuid:pk>',view_post_detail,name='post_detail'),
    path('step',view_step_detail_ajax,name='step_detail'),
    path('step/comment_create',view_step_comment_create_ajax,name='step_comment_create'),
    path('api/toggleBookMark/', toggle_bookmark_ajax),
    path('api/toggleLike/', toggle_like_ajax),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)







