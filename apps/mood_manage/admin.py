from django.contrib import admin

from .models import MoodManage, CommentManage


@admin.register(MoodManage)
class MoodManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'title', 'is_deleted', 'content', 'create_time')
    list_per_page = 100
    list_editable = ('is_deleted',)


@admin.register(CommentManage)
class CommentManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'mood_id', 'content', 'is_deleted', 'is_sec_comment', 'fir_comment_uid', 'fir_comment_nickname', 'create_time')
    list_per_page = 100
    list_editable = ('is_deleted',)
