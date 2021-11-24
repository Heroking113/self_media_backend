from __future__ import absolute_import
from celery import shared_task

from utils.common import get_7_days_before, rm_7_days_before, update_base_convert_data


@shared_task
def update_base_convert():
    """更新基础的可转债数据"""
    update_base_convert_data()


@shared_task
def update_base_convert_close_price():
    """更新基础可转债数据，同时将数据存储到本地"""
    update_base_convert_data(is_save_file=True)


@shared_task
def rm_7days_before():
    """移除超过7天的文件，避免占用过多空间"""
    rmd_filenames = get_7_days_before()
    rm_7_days_before(rmd_filenames)
    print('execute rm_7days_before()..')
