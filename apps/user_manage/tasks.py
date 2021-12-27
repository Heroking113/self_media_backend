from __future__ import absolute_import

import os
import re
from datetime import datetime

from celery import shared_task
from django.conf import settings

from utils.common import file_name_walk
from .models import AssetManage, UserManage, SchUserManage
from apps.base_convert.models import BaseConvert
from apps.bond_manage.models import OwnConvertBond
from utils.redis_cli import redisCli

@shared_task
def statistic_asset_pl():
    """
    统计每日的总资产和总盈亏:
        总资产 = sum(持有数量*现价)
        总盈亏 = sum(持有数量*(现价 - 昨日收盘价)/昨日收盘价)
    """
    uid_query = UserManage.objects.all().values('uid')
    uids = [i['uid'] for i in uid_query]
    own_query = list(OwnConvertBond.objects.filter(uid__in=uids).values('uid', 'bond_code', 'hold_num'))
    bond_codes = set([item['bond_code'] for item in own_query])
    base_convert = redisCli.get('base_convert')
    if base_convert:
        cur_bond_prices = [{'cur_bond_price': item['cur_bond_price'],
                            'yes_close_price': item['yes_close_price'],
                            'bond_code': item['bond_code']}
            for item in base_convert if item['bond_code'] in bond_codes]
    else:
        cur_bond_prices = BaseConvert.objects.filter(bond_code__in=bond_codes).values('bond_code', 'cur_bond_price', 'yes_close_price')

    # 将现价 和 昨日收盘价数据跟bond_code对应起来
    for oi in own_query:
        for cb in cur_bond_prices:
            if oi['bond_code'] == cb['bond_code']:
                oi['cur_bond_price'] = 0 if cb['cur_bond_price'] == '' or re.search(r'[a-zA-Z]', cb['cur_bond_price']) else cb['cur_bond_price']
                oi['yes_close_price'] = 0 if cb['yes_close_price'] == '' or re.search(r'[a-zA-Z]', cb['yes_close_price']) else cb['yes_close_price']
                break

    bulk_create_data = []
    for uid in uids:
        day_asset = 0
        day_pl = 0
        for oi in own_query:
            if uid == oi['uid']:
                day_asset += 0 if not oi['cur_bond_price'] else oi['hold_num'] * float(oi['cur_bond_price'])
                day_pl += 0 if not oi['cur_bond_price'] or not oi['yes_close_price'] else oi['hold_num'] * (float(oi['cur_bond_price']) - float(oi['yes_close_price'])) / float(oi['yes_close_price'])
        bulk_create_data.append(AssetManage(
            uid=uid,
            day_asset=round(day_asset, 2),
            day_pl=round(day_pl, 2),
            create_time=datetime.now()
        ))

    AssetManage.objects.bulk_create(bulk_create_data)


@shared_task
def rm_redundant_cards():
    card_root = settings.MEDIA_ROOT + '/school_card/'
    img_paths = file_name_walk(card_root)
    sch_query = SchUserManage.objects.all().values('school_card')
    sch_cards = [i['school_card'] for i in sch_query]

    for im in img_paths:
        if im not in sch_cards:
            abs_img_path = settings.MEDIA_ROOT+'/'+im
            os.remove(abs_img_path)


