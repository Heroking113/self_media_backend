from django.contrib import admin

from .models import UserManage, AssetManage


@admin.register(UserManage)
class UserManageAdmin(admin.ModelAdmin):
    list_display = ('id','uid', 'nickname', 'avatar_url', 'create_time')
    list_per_page = 100


@admin.register(AssetManage)
class AssetManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'day_asset', 'day_pl', 'create_time')
    list_per_page = 100
