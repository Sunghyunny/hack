from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import EmailField
from .validators import RegisteredEmailValidator


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'username')


class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
     # 유효성 검증 필터를 추가해 이미 인증 되거나 가입된 적이 없는 이메일이 입력될 경우 에러 발생.