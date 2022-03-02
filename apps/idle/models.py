from django.db import models

# Create your models here.
class IdleManage(models.Model):

    IDLE_TYPE = (
        ('0', 'unknown'),
        ('1', '生活用品'),
        ('2', '学习用品'),
    )

    SCHOOL = (
        ('0', 'unknown'),
    )

    uid = models.CharField(verbose_name='用户ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    phone = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号', max_length=128, blank=True, null=True)
    content = models.TextField(verbose_name='闲置描述', default='')
    price = models.IntegerField(verbose_name='价格', default=0)
    idle_type = models.CharField(verbose_name='闲置类型', max_length=8, default='0', choices=IDLE_TYPE, db_index=True)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, db_index=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    img_paths = models.TextField(verbose_name='图片路由', default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'idle'
        verbose_name_plural = verbose_name = '闲置管理'