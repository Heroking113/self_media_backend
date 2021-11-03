from django.contrib import admin

from .models import UserManage


@admin.register(UserManage)
class UserManageAdmin(admin.ModelAdmin):
    list_display = ('id','uid', 'nickname', 'avatar_url', 'create_time')
    list_per_page = 100
