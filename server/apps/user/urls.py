from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views 
from .views import user_main, user_login, user_signup, view_user_main, my_page, user_page, user_logout, kakao_Auth_Redirect, naver_Auth_Redirect

urlpatterns = [
    path('main/', user_main, name='user_main'),
    path('login/', user_login, name='user_login'), 
    path('signup/', user_signup, name='user_signup'),
    path('logout/',user_logout, name='user_logout'),
    path('',view_user_main,name='user_main'),
    path('my_page', my_page, name='my_page'),
    path('user_page/<uuid:id>', user_page, name='user_page'),
    path('kakaoRedirect/', kakao_Auth_Redirect, name='kakao_redirect'),
    path('kakaoRedirect/', kakao_Auth_Redirect, name='kakao_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)