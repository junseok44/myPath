from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',view_user_main,name='user_main'),
    path('my_page', my_page, name='my_page'),
    path('user_page/<uuid:id>', user_page, name='user_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)