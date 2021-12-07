from django.contrib import admin

from .models import IdleManage


@admin.register(IdleManage)
class IdleManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'title', 'order_status', 'is_deleted', 'sell_price', 'description', 'create_time')
    list_per_page = 100
    list_editable = ('order_status', 'is_deleted')
