from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import EmailField
from .validators import RegisteredEmailValidator
from .models import Photo
from .models import Profile
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'username')


class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
     # 유효성 검증 필터를 추가해 이미 인증 되거나 가입된 적이 없는 이메일이 입력될 경우 에러 발생.

####

class CreateUserForm(UserCreationForm): # id, pw만 입력받은 UserCreationForm을 확장시킬것이므로 상속받음
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") # 입력받을 필드순서 지정

    def save(self, commit=True):  # save메소드 오버라이드
        user = super(CreateUserForm, self).save(commit=False) # 기존의 id와 pw를 저장. commit이 Flase인 이유는 2번 저장하는것 방지.
        user.email = self.cleaned_data["email"]               # user 객체에 email 값 추가.
        if commit:
            user.save()              # 객체에 대한 모든 정보를 DB에 저장.
        return user


# 사진 업로드 폼
class UploadForm(forms.ModelForm):
    comment = forms.CharField(max_length=255)
    class Meta:
        model = Photo                         # 어떤 모델과 연결할지
        exclude = ('thumbnail_image', 'owner') # 입력받지 않을 필드를 표시가능, 이 부분은 코드로 처리해주기 위해


# 프로필사진을 업데이트할 때 사용자의 정보도 같이 업데이트 할 수 있도록 사용자정보에 대한 폼, 프로필에 대한 폼 생성
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', ]


class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False) # 선택적으로 입력할 수 있음.
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_photo', ]


class PassWordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
