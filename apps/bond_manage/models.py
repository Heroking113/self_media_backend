from django.db import models

class SelfChooseManage(models.Model):
    """自选可转债"""

    uid = models.CharField(verbose_name='用户对外ID', max_length=16)
    bond_abbr = models.CharField(verbose_name='债券简称', max_length=256)
    bond_code = models.CharField(verbose_name='债券代码', max_length=256)
    priority = models.IntegerField(verbose_name='显示的优先级', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'self_choose_manage'
        verbose_name_plural = verbose_name = '自选可转债'


class OwnConvertBond(models.Model):
    """持有可转债"""

    uid = models.CharField(verbose_name='用户对外ID', max_length=16)
    bond_abbr = models.CharField(verbose_name='债券简称', max_length=256)
    bond_code = models.CharField(verbose_name='债券代码', max_length=256)
    hold_num = models.IntegerField(verbose_name='持有数量')
    hold_cost = models.FloatField(verbose_name='持有成本')
    priority = models.IntegerField(verbose_name='显示的优先级', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'own_convert_bond'
        verbose_name_plural = verbose_name = '持有可转债'


class DayProfitLossConvertBond(models.Model):
    """
    可转债日盈亏表
        盈亏值 = 数量 * （现价 - 昨日收盘价） / 昨日收盘价
    """

    uid = models.CharField(verbose_name='用户对外ID', max_length=16)
    bond_abbr = models.CharField(verbose_name='债券简称', max_length=256)
    bond_code = models.CharField(verbose_name='债券代码', max_length=256)
    day_quote_change = models.FloatField(verbose_name='当日涨跌幅', default=0)
    day_pl = models.FloatField(verbose_name='当日盈亏', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, default=None)

    class Meta:
        db_table = 'day_profit_loss_convert_bond'
        verbose_name_plural = verbose_name = '可转债日盈亏记录'
