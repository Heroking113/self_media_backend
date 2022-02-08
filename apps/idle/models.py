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
        ('1', '深圳大学'),
        ('2', '暨南大学深圳校区'),
        ('3', '南方科技大学'),
        ('4', '哈尔滨工业大学'),
        ('5', '香港中文大学'),
        ('6', '深圳职业技术学院'),
        ('7', '深圳信息职业技术学院'),
        ('8', '中山大学'),
        ('9', '深圳理工大学'),
        ('10', '北理莫斯科大学'),
        ('11', '深圳技师学院')
    )

    uid = models.CharField(verbose_name='用户ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    phone = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号', max_length=128, blank=True, null=True)
    content = models.CharField(verbose_name='帖子内容', max_length=350, default='')
    price = models.IntegerField(verbose_name='价格', default=0)
    idle_type = models.CharField(verbose_name='帖子类型', max_length=8, default='0', choices=IDLE_TYPE)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, db_index=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    img_paths = models.TextField(verbose_name='图片路由', default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'idle'
        verbose_name_plural = verbose_name = '闲置管理'