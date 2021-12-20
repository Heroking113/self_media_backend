from django.contrib import admin

from .models import TopicManage, CommentManage


@admin.register(TopicManage)
class TopicManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'title', 'content', 'topic_type', 'school', 'is_deleted', 'create_time', 'img_paths')
    list_per_page = 100
    list_editable = ('title','content', 'is_deleted',)


@admin.register(CommentManage)
class CommentManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'inst_id', 'content', 'is_deleted', 'is_sec_comment', 'fir_comment_uid', 'fir_comment_nickname', 'create_time')
    list_per_page = 100
    list_editable = ('is_deleted',)
