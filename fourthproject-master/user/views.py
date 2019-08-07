from django.views.generic import CreateView, FormView
from .forms import UserRegistrationForm, LoginForm, VerificationEmailForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from .mixins import VerifyEmailMixin

#프로필
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required

class UserRegistrationView(VerifyEmailMixin, CreateView):
    model = get_user_model()  # 자동생성 폼에서 사용할 모델
    form_class = UserRegistrationForm  # 자동생성 폼에서 사용할 필드
    success_url = '/user/login/'
    verify_url = '/user/verify/'
    template_name = 'user/join.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/user/login/'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.', extra_tags='danger')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()     # 데이터가 변경되면 save() 호출
        return is_valid


class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = '/user/login/'
    template_name = 'user/resend_verify_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']  # 폼 객체는 유효성검증이 끝나면 cleaned_data라는 인스턴스 변수에 각 필드 이름으로 사용자가 입력한 값을 저장!
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)


class Index(TemplateView):
    template_name = 'user/home.html'

#프로필

# class ProfileView(DetailView):
#     context_object_name = 'profile_user'
#     model = User
#     template_name = 'user/user_profile.html'

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = uesr,photo_set.filter(is_public=True)[:20]
    context = {"profile_user" : user, "photos": photos}
    return render(request, 'user/user_profile')