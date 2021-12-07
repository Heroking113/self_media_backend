import logging
import re
from decimal import Decimal

from .redis_cli import redisCli

from apps.base_convert.models import BaseConvert


logger = logging.getLogger('cb_backend')


def format_bond_manage_ocb_list_ret_data(serializer_data):
    """
        格式化应用接口：bond_manage.OwnConvertBond.list
    """

    # 账户资产
    account_asset = sum([i['hold_cost'] * i['hold_num'] for i in serializer_data])

    ser_bond_codes = [item['bond_code'] for item in serializer_data]

    base_convert = redisCli.get('base_convert')
    if not base_convert:
        convert_data = BaseConvert.objects.filter(bond_code__in=ser_bond_codes).values('bond_code', 'cur_bond_price',
                                                                                       'yes_close_price')
    else:
        convert_data = [item for item in base_convert if item['bond_code'] in ser_bond_codes]

    ret_data = []
    for index, item in enumerate(serializer_data):
        dic = dict(item)

        # 现价
        cur_bond_price = [it['cur_bond_price'] for it in convert_data if it['bond_code'] == item['bond_code']][0]
        if not cur_bond_price or has_letter(cur_bond_price):
            cur_price = '-'
        else:
            cur_price = float(Decimal(str(round(float(cur_bond_price), 2))))

        # 市值
        if cur_price == '-':
            market_val = '-'
        else:
            market_val = float(Decimal(str(round(item['hold_num'] * cur_price, 2))))

        # 今日涨幅 = (现价-昨日收盘价)/昨日收盘价
        yes_close_price = [it['yes_close_price'] for it in convert_data if it['bond_code'] == item['bond_code']][0]
        if not yes_close_price or has_letter(yes_close_price):
            today_increase = '-'
        else:
            today_increase = (float(cur_price) - float(yes_close_price)) / float(yes_close_price)

        # 今日盈亏 = 数量*（现价-昨日收盘价）/昨日收盘价 = 数量 * 今日涨幅

        if today_increase == '-':
            today_pl = '-'
        else:
            today_pl = float(Decimal(str(round(item['hold_num'] * today_increase, 2))))

        # 持仓占比 = 市值 / 账户资产
        if market_val == '-':
            prop_op = '-'
        else:
            prop_op = str(Decimal(str(round(market_val / account_asset * 100, 2)))) + '%'

        # 单独处理今日涨幅
        if today_increase != '-':
            today_increase = str(Decimal(str(round(today_increase*100, 2)))) + '%'

        dic.update({
            'market_val': market_val,
            'cur_price': cur_price,
            'today_increase': today_increase,
            'today_pl': today_pl,
            'prop_op': prop_op
        })
        ret_data.append(dic)

    return ret_data


def has_letter(s):
    """判断字符串是否含有字母"""
    return True if re.search(r'[a-zA-Z]', s) else False
