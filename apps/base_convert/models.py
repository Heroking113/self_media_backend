from django.db import models

from apps.bond_manage.models import OwnConvertBond, SelfChooseManage
from utils.redis_cli import redisCli


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
    yes_close_price = models.CharField(verbose_name='昨日收盘价', max_length=256, default='')
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

    @classmethod
    def get_save_double_low_data(cls, format_data=[]):
        """
        策略：
            双低值计算公式：债现价 + 转股溢价率 * 100%
            去除双低值为零的可转债之后，经过排序得出双低值可转债列表
        """
        if not format_data:
            format_data = cls.objects.all().values(
                'bond_code',
                'bond_abbr',
                'underly_abbr',
                'underly_price',
                'conversion_price',
                'conversion_value',
                'cur_bond_price',
                'yes_close_price',
                'conversion_preminum_rate')

        for item in format_data:
            cur_bond_price = float(item['cur_bond_price']) if item['cur_bond_price'] else 0
            conversion_preminum_rate = float(item['conversion_preminum_rate']) if item['conversion_preminum_rate'] else 0
            dl_val = cur_bond_price + conversion_preminum_rate
            item['dl_val'] = round(dl_val, 3)

            if item['conversion_value']:
                item['conversion_value']=round(float(item['conversion_value']), 3)
            if item['conversion_preminum_rate']:
                item['conversion_preminum_rate']=round(float(item['conversion_preminum_rate']), 3)


        # 去除双低值为零的可转债
        except_zero_data = [item for item in format_data if item['dl_val']]

        # 通过 双低值 对可转债进行排序
        dl_data = sorted(except_zero_data, key = lambda e:e.__getitem__('dl_val'))

        # 将双低数据和页数存到redis
        dl_pages = len(dl_data) // 20 if not len(dl_data) % 20 else len(dl_data) // 20 + 1
        dl_data = [dl_data[i*20: (i+1)*20] for i in range(dl_pages)]
        redisCli.set('dl_pages', dl_pages)
        redisCli.set('dl_data', dl_data)

        return {
            'next': '/bc/double_low_data/?page=2',
            'results': dl_data[0]
        }

    @classmethod
    def format_ret_data(cls, uid, ser_data):
        held_query = OwnConvertBond.objects.filter(uid=uid).values('bond_code')
        held_codes = [item['bond_code'] for item in held_query]
        chosen_query = SelfChooseManage.objects.filter(uid=uid).values('bond_code')
        chosen_codes = [item['bond_code'] for item in chosen_query]

        for s in ser_data:
            s['hold_status'] = ''
            if s['bond_code'] in chosen_codes:
                s['hold_status'] = 'chosen'
            if s['bond_code'] in held_codes:
                s['hold_status'] = 'held'

        return ser_data

    @classmethod
    def get_base_convert_in_codes(cls, bond_codes=[]):
        base_convert = redisCli.get('base_convert')
        if base_convert:
            return [item for item in base_convert if item['bond_code'] in bond_codes] if bond_codes else base_convert
        base_convert = list(cls.objects.all())
        return [dict(i) for i in base_convert if i.bond_code in bond_codes] if bond_codes else [dict(i) for i in base_convert]
