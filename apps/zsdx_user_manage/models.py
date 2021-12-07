from django.db import models

# Create your models here.
class ZsdxUserManage(models.Model):
    GENDER = (
        ('0', 'unknown'),
        ('1', '男'),
        ('2', '女')
    )

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='')
    avatar_url = models.TextField(verbose_name='头像地址', default='')
    wechat = models.CharField(verbose_name='微信', max_length=128, default='')
    mobile = models.CharField(verbose_name='手机号', max_length=11, default='')
    unionid = models.CharField(max_length=256, verbose_name='unionId', blank=True, null=True)
    openid = models.CharField(max_length=256, verbose_name='openId', blank=True, null=True)
    session_key = models.CharField(max_length=256, verbose_name='session_key', blank=True, null=True)
    gender = models.CharField(verbose_name='性别', max_length=16, choices=GENDER, default='0')
    city = models.CharField(max_length=64, verbose_name='城市', blank=True, null=True)
    province = models.CharField(max_length=64, verbose_name='省份', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'zsdx_user_manage'
        verbose_name_plural = verbose_name = '中山大学用户管理'