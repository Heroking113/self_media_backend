from django.db import models

# Create your models here.
class BaseConvert(models.Model):
    bond_code = models.CharField(verbose_name='债券代码', max_length=256, default='')
    bond_abbr = models.CharField(verbose_name='债券简称', max_length=256, default='')
    purchase_date = models.CharField(verbose_name='申购日期', max_length=256, default='')
    purchase_code = models.CharField(verbose_name='申购代码', max_length=256, default='')
    purchase_limit = models.CharField(verbose_name='申购上限', max_length=256, default='')
    underly_code = models.CharField(verbose_name='正股代码', max_length=256, default='')
    underly_abbr = models.CharField(verbose_name='正股简称', max_length=256, default='')
    underly_price = models.CharField(verbose_name='正股价', max_length=256, default='')
    conversion_price = models.CharField(verbose_name='转股价', max_length=256, default='')
    conversion_value = models.CharField(verbose_name='转股价值', max_length=256, default='')
    cur_bond_price = models.CharField(verbose_name='债现价', max_length=256, default='')
    conversion_preminum_rate = models.CharField(verbose_name='转股溢价率', max_length=256, default='')
    abos_erd = models.CharField(verbose_name='原股东配售-股权登记日', max_length=256, default='')
    abos_aps = models.CharField(verbose_name='原股东配售-每股配售额', max_length=256, default='')
    issurance_scale = models.CharField(verbose_name='发行规模', max_length=256, default='')
    ido_wln = models.CharField(verbose_name='中签号发布日', max_length=256, default='')
    win_rate = models.CharField(verbose_name='中签率', max_length=256, default='')
    time_market = models.CharField(verbose_name='上市时间', max_length=256, default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lasted_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'base_convert'
        verbose_name_plural = verbose_name = '基础可转债信息表'

