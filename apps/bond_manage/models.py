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

    @staticmethod
    def handle_serializer_data(serializer_data):
        ret_data = []
        for item in serializer_data:
            dic = item
            # 市值
            market_val = '市值'
            # 现价
            cur_price = '现价'
            # 今日涨幅
            today_increase = '今日涨幅'
            # 今日盈亏
            today_pl = '今日盈亏'
            # 持仓占比
            prop_op = '持仓占比'

            dic.update({
                'market_val': market_val,
                'cur_price': cur_price,
                'today_increase': today_increase,
                'today_pl': today_pl,
                'prop_op': prop_op
            })
            ret_data.append(dic)

        return ret_data


class DayProfitLossConvertBond(models.Model):
    """可转债日盈亏表"""

    uid = models.CharField(verbose_name='用户对外ID', max_length=16)
    convert_id = models.IntegerField(verbose_name='可转债ID')
    bond_abbr = models.CharField(verbose_name='债券简称', max_length=256)
    bond_code = models.CharField(verbose_name='债券代码', max_length=256)
    quote_change = models.FloatField(verbose_name='涨跌幅', default=0)
    pre_day_fund = models.FloatField(verbose_name='昨日总资金', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, default=None)

    class Meta:
        db_table = 'day_profit_loss_convert_bond'
        verbose_name_plural = verbose_name = '可转债日盈亏记录'


    @staticmethod
    def format_res_data(ownConvertIds, serializer_data):
        ret_data = []
        for oi in ownConvertIds:
            sum_quote_change = 0
            sum_pl = 0
            bond_abbr = ''
            for si in serializer_data:
                if si['convert_id'] == oi['id']:
                    sum_quote_change += si['quote_change']
                    sum_pl += si['pre_day_fund']
                    bond_abbr = si['bond_abbr']
            ret_data.append({
                'bond_abbr': bond_abbr,
                'sum_quote_change': round(sum_quote_change * 100, 2),
                'sum_pl': sum_pl
            })

        return ret_data
