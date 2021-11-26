from __future__ import absolute_import

from datetime import datetime

from celery import shared_task

from .models import AssetManage, UserManage
from apps.base_convert.models import BaseConvert
from apps.bond_manage.models import OwnConvertBond
from utils.redis_cli import RedisCli

@shared_task
def statistic_asset_pl():
    """
    统计每日的总资产和总盈亏:
        总资产 = sum(持有数量*现价)
        总盈亏 = sum(持有数量*(现价 - 昨日收盘价)/昨日收盘价)
    """
    uid_query = UserManage.objects.all().values('uid')
    uids = [item['uid'] for item in uid_query]
    own_query = OwnConvertBond.objects.filter(uid__in=uids).values('uid', 'bond_code', 'hold_num')
    bond_codes = [item['bond_code'] for item in own_query]
    base_convert = RedisCli.get('base_convert')
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
                oi['cur_bond_price'] = cb['bond_code']
                oi['yes_close_price'] = cb['yes_close_price']
                break

    bulk_create_data = []
    for uid in uids:
        day_asset = 0
        day_pl = 0
        for oi in own_query:
            if uid == oi['uid']:
                day_asset += 0 if not oi['cur_bond_price'] else oi['hold_num'] * float(oi['cur_bond_price'])
                day_pl += 0 if not oi['cur_bond_price'] or not oi['yes_close_price'] else oi['hold_hum'] * (float(oi['cur_bond_price']) - float(oi['yes_close_price'])) / float(oi['yes_close_price'])
        bulk_create_data.append(AssetManage(
            uid=uid,
            day_asset=round(day_asset, 2),
            day_pl=round(day_pl, 2),
            create_time=datetime.now()
        ))

    AssetManage.objects.bulk_create(bulk_create_data)








