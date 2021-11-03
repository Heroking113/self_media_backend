from django.db import models

from utils.common import set_uid


class UserManage(models.Model):
    GENDER = (
        ('0', 'unknown'),
        ('1', '男'),
        ('2', '女')
    )

    uid = models.CharField(verbose_name='用户对外的ID', max_length=16, default=set_uid())
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='')
    avatar_url = models.TextField(verbose_name='头像地址', default='')
    unionid = models.CharField(max_length=256, verbose_name='unionId', blank=True, null=True)
    openid = models.CharField(max_length=256, verbose_name='openId', blank=True, null=True)
    session_key = models.CharField(max_length=256, verbose_name='session_key', blank=True,null=True)
    gender = models.IntegerField(verbose_name='性别', choices=GENDER, default='0')
    city = models.CharField(max_length=64, verbose_name='城市', blank=True, null=True)
    province = models.CharField(max_length=64, verbose_name='省份', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建的时间', help_text='创建的时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='最后一次更新的时间', help_text='最后一次更新的时间')

    class Meta:
        db_table = 'user_manage'
        verbose_name_plural = verbose_name = '用户管理'


class AssetManage(models.Model):
    uid = models.CharField(verbose_name='用户对外的ID', max_length=16, default=set_uid())

    class Meta:
        db_table = 'asset_manage'
        verbose_name_plural = verbose_name = '用户资产管理'
