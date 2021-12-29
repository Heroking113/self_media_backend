from django.contrib import admin

from .models import UserManage, AssetManage, SchUserManage


@admin.register(SchUserManage)
class SchUserManageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'uid',
                    'nickname',
                    'school',
                    'wechat',
                    'mobile',
                    'authenticate_status',
                    'school_card',
                    'avatar_url',
                    'openid',
                    'unionid',
                    'create_time',
                    'lasted_time')

    list_editable = ('authenticate_status',)

    list_filter = ('school', 'authenticate_status')

    list_per_page = 50


@admin.register(UserManage)
class UserManageAdmin(admin.ModelAdmin):
    list_display = ('id','uid', 'nickname', 'avatar_url', 'create_time')
    list_per_page = 50


@admin.register(AssetManage)
class AssetManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'day_asset', 'day_pl', 'create_time')
    list_per_page = 50
