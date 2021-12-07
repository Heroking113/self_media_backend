from django.db import models

# Create your models here.
class MoodManage(models.Model):

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    title = models.CharField(max_length=32, verbose_name='帖子标题', default='', null=True, blank=True)
    content = models.CharField(verbose_name='帖子内容', max_length=512, default='')
    view_count = models.IntegerField(verbose_name='浏览量', default=0)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    img_paths = models.TextField(verbose_name='图片路由', default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'mood_manage'
        verbose_name_plural = verbose_name = '帖子管理'


class CommentManage(models.Model):
    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    mood_id = models.IntegerField(verbose_name='帖子ID', default=0)
    content = models.CharField(verbose_name='评论内容', max_length=256, default='')
    is_sec_comment = models.BooleanField(verbose_name='是否二级评论', default=False, null=True, blank=True)
    fir_comment_uid = models.CharField(verbose_name='一级评论ID', max_length=16, default='', null=True, blank=True)
    fir_comment_nickname = models.CharField(verbose_name='用户昵称', max_length=32, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'comment_manage'
        verbose_name_plural = verbose_name = '评论管理'
