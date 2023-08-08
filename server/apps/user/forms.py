from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('loginId', 'username', 'email', 'password1', 'password2', 'intro', 'membership')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('loginId', 'username', 'email', 'intro', 'membership')