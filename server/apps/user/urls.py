from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views 
from .views import *

urlpatterns = [
    path('main/', user_main, name='user_main'),
    path('login/', user_login, name='user_login'), 
    path('signup/', user_signup, name='user_signup'),
    path('logout/',user_logout, name='user_logout'),
    path('login/find_id/',find_id, name='find_id'),
    path('login/reset_pw/',reset_password, name='reset_password'),
    path('my_page', my_page, name='my_page'),
    path('user_page/<uuid:id>', user_page, name='user_page'),
    path('profile',user_profile,name="edit_profile"),
    path('addCard',user_card_add, name="user_card_add"),
    path('userIntro', user_intro_update, name="user_intro_update"),
    path('deleteCard/<int:id>',user_card_delete,name="user_card_delete"),
    path('updateCard/<int:id>',user_card_edit,name="user_card_edit"),
    path('googleLoginStart', google_Auth_Start, name="google_start"),
    path('googleRedirect/', google_Auth_Redirect, name="google_redirect"),
    path('kakaoRedirect/', kakao_Auth_Redirect, name='kakao_redirect'),
    path('user_info/<uuid:id>', user_info, name='user_info'),
    path('user_delete/', user_delete, name='user_delete'),
    path('user_pw_edit/', user_pw_edit, name='user_pw_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)