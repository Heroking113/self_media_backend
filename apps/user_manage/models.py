from django.db import models, transaction

from utils.tencent_sdk import tencent_ocr


class SchUserManage(models.Model):

    SCHOOL = (
        ('0', 'unknown'),
        ('1', '深圳大学'), # 二批
        ('2', '暨南大学深圳校区'), # 一批
        ('3', '南方科技大学'), # 一批
        ('4', '哈尔滨工业大学'), # 二批
        ('5', '香港中文大学'), # 三批
        ('6', '深圳职业技术学院'), # 二批
        ('7', '深圳信息职业技术学院'), # 一批
        ('8', '中山大学'), # 二批
        ('9', '深圳理工大学'), # 三批
        ('10', '北理莫斯科大学'), # 三批
        ('11', '深圳技师学院') # 一批
    )

    AUTHENTICATE_STATUS = (
        ('1', '初次登录'),
        ('2', '定位采集中'),
        ('3', '人工审核中'),
        ('4', '非本校用户'),
        ('5', '本校用户')
    )


    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='昵称', max_length=64, default='')
    avatar_url = models.TextField(verbose_name='头像地址', default='')
    wechat = models.CharField(verbose_name='微信', max_length=128, default='')
    mobile = models.CharField(verbose_name='手机号', max_length=11, default='')
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, null=True, blank=True, db_index=True)
    unionid = models.CharField(max_length=256, verbose_name='unionId', blank=True, null=True)
    openid = models.CharField(max_length=256, verbose_name='openId', blank=True, null=True)
    session_key = models.CharField(max_length=256, verbose_name='session_key', blank=True, null=True)
    authenticate_status = models.CharField(verbose_name='认证状态', max_length=8, choices=AUTHENTICATE_STATUS, default='1')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sch_user_manage'
        verbose_name_plural = verbose_name = '高校用户管理'


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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_manage'
        verbose_name_plural = verbose_name = '可转债用户管理'


class AssetManage(models.Model):
    """资产管理：每天下午15：10统计一遍
        当日总资产 = sum(可转债现价 * 持有的可转债数量)
            如果删除A可转债，当日总资产 = 现有总资产 - A可转债现价 * 持有数量
        当日盈亏 = sum(持有的可转债A的数量 *（可转债A的现价-可转债A的昨日收盘价）/ 可转债A的昨日收盘价)
            如果删除A可转债，当日盈亏不影响
    """

    uid = models.CharField(verbose_name='用户对外的ID', max_length=16, default='')
    day_asset = models.DecimalField(verbose_name='当日总资产', max_digits=13, decimal_places=2, default=0)
    day_pl = models.DecimalField(verbose_name='当日盈亏', max_digits=13, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, default=None)

    class Meta:
        db_table = 'asset_manage'
        verbose_name_plural = verbose_name = '可转债用户资产管理'
