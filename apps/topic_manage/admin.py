from django.contrib import admin

from .models import TopicManage, CommentManage


@admin.register(TopicManage)
class TopicManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'topic_type', 'school', 'is_deleted', 'title', 'content', 'create_time', 'img_paths')
    list_per_page = 50
    list_editable = ('topic_type', 'is_deleted', 'title', 'content')
    list_filter = ('school', 'topic_type')
    search_fields = ('title', 'content')


@admin.register(CommentManage)
class CommentManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'is_deleted', 'nickname', 'inst_id', 'content', 'is_sec_comment', 'fir_comment_uid', 'fir_comment_nickname', 'create_time')
    list_per_page = 50
    list_editable = ('is_deleted',)
