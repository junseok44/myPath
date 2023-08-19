from django.contrib.auth.backends import ModelBackend
from .models import User 

class LoginIDBackend(ModelBackend):
    def authenticate(self, request, loginId=None, password=None, **kwargs):
        try:
            user = User.objects.get(loginId=loginId)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None