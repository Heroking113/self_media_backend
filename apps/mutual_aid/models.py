from django.db import models

# Create your models here.
class MutualManage(models.Model):

    MUT_TYPE = (
        ('0', 'unknown'),
        ('1', '代拿快递'),
        ('2', '代拿外卖'),
        ('3', '寻物启事'),
        ('4', '失物招领'),
        ('5', '其他')
    )

    SCHOOL = (
        ('0', 'unknown'),
    )

    uid = models.CharField(verbose_name='用户ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    phone = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号', max_length=128, blank=True, null=True)
    content = models.TextField(verbose_name='互助描述', default='')
    salary = models.IntegerField(verbose_name='价格', default=0)
    mut_type = models.CharField(verbose_name='互助类型', max_length=8, default='0', choices=MUT_TYPE, db_index=True)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, db_index=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    img_paths = models.TextField(verbose_name='图片路由', default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'mutual'
        verbose_name_plural = verbose_name = '互助管理'
