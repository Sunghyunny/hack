from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('create/', views.UserRegistrationView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', views.UserVerificationView.as_view()),
    path('resend_verify_email/', views.ResendVerifyEmailView.as_view(), name='resend'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_reset(ch).html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    ###프로필###
    path('profile/<int:pk>/', views.profile, name='profile'),
    # path('upload', views.upload, name='upload'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
    ]