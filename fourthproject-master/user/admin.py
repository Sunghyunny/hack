from django.contrib import admin
from .models import User

#프로필
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
from .models import Photo
from .models import Profile



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name','username', 'joined_at', 'last_login_at', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email', 'name')
    exclude = ('password',)                           # 사용자 상세 정보에서 비밀번호 필드를 노출하지 않음

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    joined_at.admin_order_field = '-date_joined'      # 가장 최근에 가입한 사람부터 리스팅
    joined_at.short_description = '가입일'
    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근로그인'

#프로필
class ProfileInline(admin.StackedInline): # 로또 프로젝트에서 썼던 방식으로 유저 밑에 프로필 을 붙여서 보여주려고 이를 상속받음
    model = Profile
    con_delete = False                    # 프로필을 아예 없앨 수 없게 하는 속성(한번 만들면 지우는건 이상하니까)

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


# class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
#     inlines = (ProfileInline,)
#     list_display = ('id', 'email', 'name', 'username', 'joined_at', 'last_login_at', 'is_superuser', 'is_active')
#     list_display_links = ('id', 'email', 'name')
#     exclude = ('password',)  # 사용자 상세 정보에서 비밀번호 필드를 노출하지 않음
#
#     def joined_at(self, obj):
#         return obj.date_joined.strftime("%Y-%m-%d")
#
#     def last_login_at(self, obj):
#         if not obj.last_login:
#             return ''
#         return obj.last_login.strftime("%Y-%m-%d %H:%M")
#
#     joined_at.admin_order_field = '-date_joined'  # 가장 최근에 가입한 사람부터 리스팅
#     joined_at.short_description = '가입일'
#     last_login_at.admin_order_field = 'last_login_at'
#     last_login_at.short_description = '최근로그인'
#

admin.site.register(Photo)
# 기존의 User의 등록을 취소했다가 User와 ProfileInline을 붙임.
admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
