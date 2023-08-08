from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', view_post_main, name='post_main'),
    path('post/write', view_post_write, name="post_write"),
    path('post/edit/<uuid:id>', view_post_edit, name="post_edit"),
    path('post/delete/<uuid:id>', view_post_delete, name="post_delete"),
    path('post/list', view_post_list, name="post_list")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
