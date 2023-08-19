from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'post'

urlpatterns = [
    path('', view_post_main, name='post_main'),
    path('post/write', view_post_write, name="post_write"),
    path('post/edit/<uuid:id>', view_post_edit, name="post_edit"),
    path('post/delete/<uuid:id>', view_post_delete, name="post_delete"),
    path('post/list', view_post_list, name="post_list"),
    path('post/<uuid:pk>',view_post_detail,name='post_detail'),
    path('post/step',view_step_detail_ajax,name='step_detail'),
    path('post/step/create_comment',view_step_create_comment_ajax,name='step_create_comment'),
    path('post/<uuid:pk>/create_comment',view_post_create_comment,name='post_create_comment'),
    path('post/delete_comment',view_post_delete_comment_ajax,name='post_delete_comment'),
    path('post/step/delete_comment',view_step_delete_comment_ajax,name='step_delete_comment'),
    path("category/<int:category_id>/", category_search , name='category'),
    path('api/toggleBookMark/', toggle_bookmark_ajax),
    path('api/toggleLike/', toggle_like_ajax),
    path('search/', search , name='search'),
    path('search/category/', search_by_category , name='search_by_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)



