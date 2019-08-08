from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
)
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

#프로필
from django.conf import settings
from sorl.thumbnail import ImageField


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), unique=True, blank=False)
    name = models.CharField('이름', max_length=30, blank=True)
    username = models.CharField('아이디', max_length=30, unique=True, blank=True)
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # email을 사용자의 식별자로 설정, user 모델에서 필드의 이름을 설명하는 문자열이다. 유니크 식별자로 사용됨.
    REQUIRED_FIELDS = ['username']  # 필수입력값(createsuperuser 커맨드로 유저를 생성할 때 나타날 필드 이름 목록

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def email_user(self, subject, message, from_email=None, **kwargs):  # 이메일 발송 메소드
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UsersManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
         extra_fields.setdefault('is_staff', True)
         extra_fields.setdefault('is_superuser', True)

         if extra_fields.get('is_staff') is not True:
             raise ValueError('Superuser must have is_staff=True.')
         if extra_fields.get('is_superuser') is not True:
             raise ValueError('Superuser must have is_superuser=True.')

         return self._create_user(email, password, **extra_fields)

# Create your models here.

#프로필

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    profile_photo = models.ImageField(blank=True)


def user_path(instance, filename): # instance는 Photo 클래스의 객체, filename은 업로드할 파일의 파일이름
    from random import choice   # string으로 나온 결과에서 하나의 문자열만 뽑아냄
    import string               # 무작위 문자열을 뽑아내기 위한 용도
    arr = [choice(string.ascii_letters) for _ in range(8)] # 무작위로 8글자를 뽑아줌
    pid = ''.join(arr)          # 파일 아이디생성
    extension = filename.split('.')[-1] # 파일이름으로부터 확장자명가져오기
    # ex) honux/asfqqwer.png
    return '%s/%s.%s' % (instance.owner.username, pid, extension)


class Photo(models.Model):
    image = models.ImageField(upload_to=user_path)      # upload_to로 어디에 업로드할지 지정할 수 있음.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 하나의 사진은 한명의 사용자에게 속해야 하므로. 1:N의 관계
    # thumbnail_image = models.ImageField(blank=True)      # blank가 True이면 폼 입력시 꼭 입력하지 않아도 된다는 의미
    comment = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)  # 사용자가 입력하지 않고 업로드 하는 순간 자동으로 세팅이 됨.
    is_public = models.BooleanField(default=False)      # 비공개 사진인지, 공개 사진인지에 대한 필드

    # 객체를 출력하면 보고싶은 내용 수정(함수 오버라이딩)
    def __str__(self):
        return '{} {} {}'.format(self.owner, self.comment, self.is_public)