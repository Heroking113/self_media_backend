from __future__ import absolute_import

import re
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.db.models import Q

from apps.base_convert.models import BaseConvert
from apps.bond_manage.models import OwnConvertBond, DayProfitLossConvertBond


@shared_task
def statistic_day_bond_pl():
    """统计每只可转债日盈亏表"""
    own_query = OwnConvertBond.objects.all().values('uid', 'bond_code', 'bond_abbr', 'hold_num')
    bond_codes = [i['bond_code'] for i in own_query]
    base_query = BaseConvert.objects.filter(bond_code__in=bond_codes).values('bond_code', 'cur_bond_price', 'yes_close_price')
    bulk_update_data = []
    for item in own_query:
        for jtm in base_query:
            if item['bond_code'] == jtm['bond_code']:
                cur_bond_price = 0 if jtm['cur_bond_price'] == '' or re.search(r'[a-zA-Z]', jtm['cur_bond_price']) else jtm[
                    'cur_bond_price']
                yes_close_price = 0 if jtm['yes_close_price'] == '' or re.search(r'[a-zA-Z]', jtm['yes_close_price']) else jtm['yes_close_price']
                if not yes_close_price:
                    day_quote_change = 0
                else:
                    day_quote_change = (float(cur_bond_price) - float(yes_close_price)) / float(yes_close_price)
                day_pl = item['hold_num'] * day_quote_change
                bulk_update_data.append(DayProfitLossConvertBond(**{
                    'uid': item['uid'],
                    'bond_code': item['bond_code'],
                    'bond_abbr': item['bond_abbr'],
                    'day_quote_change': round(day_quote_change, 4),
                    'day_pl': round(day_pl, 2),
                    'create_time': datetime.now()
                }))
                break

    DayProfitLossConvertBond.objects.bulk_create(bulk_update_data)
