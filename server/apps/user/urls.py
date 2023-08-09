from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import user_main, user_login, user_signup

urlpatterns = [
    path('', user_main, name='user_main'),
    path('login/', user_login, name='user_login'), 
    path('signup/', user_signup, name='user_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)