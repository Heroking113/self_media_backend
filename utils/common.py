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
from .redis_cli import redisCli

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


def handle_rm_7_days_before(rmd_filenames):
    """移除一周前的一周数据"""
    file_path = str(settings.BASE_DIR) + '/media/base_convert_data/'
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
    """
    更新可转债基础数据:
        1. 存入mysql 和 redis（每天更新数次）
        2. 存入本地文档（每天更新一次，七天之后删除）
    """

    to_redis_base_convert = []
    with transaction.atomic():
        bond_zh_cov_df = ak.bond_zh_cov()
        base_convert_list_to_insert = list()

        # 用以获取昨日收盘价
        ini_filename = (datetime.today() + timedelta(-1)).strftime('%Y-%m-%d') + '-可转债数据.csv'
        ini_path_root = str(settings.BASE_DIR) + '/media/base_convert_data/'
        ini_path = ini_path_root + ini_filename
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

            # 将行数据格式化成字典
            row_data = base_convert_li_dic(r, yes_close_price)
            # 将数据存入redis缓存，增加读写效率
            to_redis_base_convert.append(row_data)
            # 将数据存入mysql数据库
            base_convert_list_to_insert.append(BaseConvert(**row_data))

        # 存入redis
        redisCli.set('base_convert', to_redis_base_convert)

        # 先删除，再重新创建
        BaseConvert.objects.all().delete()
        BaseConvert.objects.bulk_create(base_convert_list_to_insert)

    # 将双低数据存到redis
    BaseConvert.get_save_double_low_data(to_redis_base_convert)

    # 将数据存到mysql
    if is_save_file:
        # 将新的数据存储到本地文档
        tar_filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '-可转债数据.csv'
        tar_path = str(settings.BASE_DIR) + '/media/base_convert_data/' + tar_filename
        bond_zh_cov_df.to_csv(tar_path)


def base_convert_li_dic(li, yes_close_price):
    dic = {
        'bond_code': str(li[0]),
        'bond_abbr': str(li[1]),
        'purchase_date': str(li[2]),
        'purchase_code': str(li[3]),
        'purchase_limit': str(li[4]),
        'underly_code': str(li[5]),
        'underly_abbr': str(li[6]),
        'underly_price': '' if str(li[7]) == 'nan' else str(li[7]),
        'conversion_price': '' if str(li[8]) == 'nan' else str(li[8]),
        'conversion_value': '' if str(li[9]) == 'nan' else str(li[9]),
        'cur_bond_price': '' if str(li[10]) == 'nan' else str(li[10]),
        'yes_close_price': yes_close_price,
        'conversion_preminum_rate': '' if str(li[11]) == 'nan' else str(li[11]),
        'abos_erd': str(li[12]),
        'abos_aps': str(li[13]),
        'issurance_scale': '' if str(li[14]) == 'nan' else str(li[14]),
        'ido_wln': str(li[15]),
        'win_rate': '' if str(li[16]) == 'nan' else str(li[16]),
        'time_market': '' if str(li[17]) == 'NaT' else str(li[17])
    }
    return dic


def datetime_format(datetime):
    date, tim_ = datetime.split('T')
    return ' '.join([date, tim_.split('.')[0]])


def change_img_size(file_path, compress_rate=0.6):
    from PIL import Image
    import io
    img = Image.open(file_path)
    img_byteArr = io.BytesIO()
    img.save(img_byteArr, format='png')
    buffer = img_byteArr.getvalue()
    kb_size = len(buffer) / 1e3

    while kb_size > 500:
        w, h = img.size
        img = img.resize((int(w*compress_rate), int(h*compress_rate)))
        img_byteArr = io.BytesIO()
        img.save(img_byteArr, format='png')
        buffer = img_byteArr.getvalue()
        kb_size = len(buffer) / 1e3

    return buffer