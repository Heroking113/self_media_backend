import random
import string
import time
import os
import logging
from datetime import timedelta, datetime

import pandas as pd
import akshare as ak
from django.db import transaction
from django.conf import settings

from apps.base_convert.models import BaseConvert

BASE_DIR = str(settings.BASE_DIR)

logger = logging.getLogger('cb_backend')


def get_7_days_before():
    """获取前7天的日期"""

    rmd_filenames = []
    for i in range(7, 14):
        day = datetime.now() - timedelta(days=i)
        n_day = datetime(day.year, day.month, day.day).strftime('%Y-%m-%d')
        rmd_filenames.append(n_day+'-可转债数据.csv')

    return rmd_filenames


def rm_7_days_before(rmd_filenames):
    """移除一周前的一周数据"""
    file_path = BASE_DIR + '/media/'
    filenames = os.listdir(file_path)
    for itm in filenames:
        if itm in rmd_filenames:
            os.unlink(file_path+itm)


def set_uid():
    """设置用户对外的ID"""
    rt = time.strftime("%H%M%S%MS",time.localtime(time.time()))
    t = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(9)).lower()
    return ''.join([rt[4], t, rt[5]])


def update_base_convert_data(is_save_file=False):
    """更新可转债基础数据"""

    with transaction.atomic():
        bond_zh_cov_df = ak.bond_zh_cov()
        base_convert_list_to_insert = list()

        ini_filename = (datetime.today() + timedelta(-1)).strftime('%Y-%m-%d') + '-可转债数据.csv'
        ini_path = str(settings.BASE_DIR) + '/media/' + ini_filename
        csv_data = pd.read_csv(ini_path, low_memory=False)
        csv_df = pd.DataFrame(csv_data)

        for r in bond_zh_cov_df.values:
            bond_code = str(r[0])
            yes_close_price = ''

            li_bond_code = list(csv_df['债券代码'])
            li_cur_bond_price = list(csv_df['债现价'])

            for idx, itm in enumerate(li_bond_code):
                if str(itm) == bond_code:
                    yes_close_price = str(li_cur_bond_price[idx])
                    break

            base_convert_list_to_insert.append(BaseConvert(
                bond_code=str(r[0]),
                bond_abbr=str(r[1]),
                purchase_date=str(r[2]),
                purchase_code=str(r[3]),
                purchase_limit=str(r[4]),
                underly_code=str(r[5]),
                underly_abbr=str(r[6]),
                underly_price='' if str(r[7]) == 'nan' else str(r[7]),
                conversion_price='' if str(r[8]) == 'nan' else str(r[8]),
                conversion_value='' if str(r[9]) == 'nan' else str(r[9]),
                cur_bond_price='' if str(r[10]) == 'nan' else str(r[10]),
                yes_close_price=yes_close_price,
                conversion_preminum_rate='' if str(r[11]) == 'nan' else str(r[11]),
                abos_erd=str(r[12]),
                abos_aps=str(r[13]),
                issurance_scale='' if str(r[14]) == 'nan' else str(r[14]),
                ido_wln=str(r[15]),
                win_rate='' if str(r[16]) == 'nan' else str(r[16]),
                time_market='' if str(r[17]) == 'NaT' else str(r[17])
            ))

        # 先删除，再重新创建
        BaseConvert.objects.all().delete()
        BaseConvert.objects.bulk_create(base_convert_list_to_insert)

    if is_save_file:
        # 将新的数据存储到本地文档
        tar_filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '-可转债数据.csv'
        tar_path = str(settings.BASE_DIR) + '/media/' + tar_filename
        bond_zh_cov_df.to_csv(tar_path)


def datetime_format(datetime):
    date, tim_ = datetime.split('T')
    return ' '.join([date, tim_.split('.')[0]])


def handle_serializer_data(serializer_data):
    li_data = serializer_data
    ret_data = []
    for item in serializer_data:
        dic = dict(item)

        # 市值
        market_val = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
        # 现价
        cur_price = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
        # 今日涨幅
        today_increase = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
        # 今日盈亏
        today_pl = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
        # 持仓占比
        prop_op = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))

        dic.update({
            'market_val': market_val,
            'cur_price': cur_price,
            'today_increase': today_increase,
            'today_pl': today_pl,
            'prop_op': prop_op
        })
        ret_data.append(dic)

    return ret_data
