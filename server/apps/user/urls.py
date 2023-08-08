from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .views import view_user_login, view_user_signup

urlpatterns = [
    path('login/', view_user_login, name='login'),
    path('signup/', view_user_signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)