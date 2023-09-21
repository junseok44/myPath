from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('loginId', 'username', 'password1', 'password2')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'intro')

class UserInfoModifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['loginId', 'username', 'intro', 'kakaoId', 'googleId', 'naverId']

    def __init__(self, *args, **kwargs):
        super(UserInfoModifyForm, self).__init__(*args, **kwargs)
        # 소셜 로그인 필드는 비활성화
        self.fields['kakaoId'].widget.attrs['readonly'] = True
        self.fields['googleId'].widget.attrs['readonly'] = True
        self.fields['naverId'].widget.attrs['readonly'] = True
