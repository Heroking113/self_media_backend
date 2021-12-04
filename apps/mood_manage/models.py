from django.db import models

# Create your models here.
class MoodManage(models.Model):

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    title = models.CharField(max_length=32, verbose_name='物品名称', help_text='物品名称', default='')
    description = models.CharField(verbose_name='物品描述', help_text='物品描述', max_length=512, default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'mood_manage'
        verbose_name_plural = verbose_name = '帖子管理'
