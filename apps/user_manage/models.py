from time import timezone

from django.db import models


class UserManage(models.Model):
    GENDER = (
        ('0', 'unknown'),
        ('1', '男'),
        ('2', '女')
    )

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='')
    avatar_url = models.TextField(verbose_name='头像地址', default='')
    unionid = models.CharField(max_length=256, verbose_name='unionId', blank=True, null=True)
    openid = models.CharField(max_length=256, verbose_name='openId', blank=True, null=True)
    session_key = models.CharField(max_length=256, verbose_name='session_key', blank=True,null=True)
    gender = models.CharField(verbose_name='性别', max_length=16, choices=GENDER, default='0')
    city = models.CharField(max_length=64, verbose_name='城市', blank=True, null=True)
    province = models.CharField(max_length=64, verbose_name='省份', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_manage'
        verbose_name_plural = verbose_name = '用户管理'


class AssetManage(models.Model):
    """资产管理"""

    uid = models.CharField(verbose_name='用户对外的ID', max_length=16, default='')
    day_asset = models.DecimalField(verbose_name='当日总资产', max_digits=13, decimal_places=2, default=0)
    day_pl = models.DecimalField(verbose_name='当日盈亏', max_digits=13, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, default=None)

    class Meta:
        db_table = 'asset_manage'
        verbose_name_plural = verbose_name = '用户资产管理'
