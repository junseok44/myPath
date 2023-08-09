from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import user_main, user_login, user_signup, view_user_main, my_page, user_page

urlpatterns = [
    path('main/', user_main, name='user_main'),
    path('login/', user_login, name='user_login'), 
    path('signup/', user_signup, name='user_signup'),
    path('',view_user_main,name='user_main'),
    path('my_page', my_page, name='my_page'),
    path('user_page/<uuid:id>', user_page, name='user_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)