from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ['id', 'username', 'email', 'date_joined','get_phone']
    empty_value_display = '-empty-'

    def get_phone(self, obj):
        result = obj.profile.phone
        return result

    get_phone.short_description = 'Phone Number'


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)