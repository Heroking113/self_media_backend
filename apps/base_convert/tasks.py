from __future__ import absolute_import
from celery import shared_task

from utils.common import get_7_days_before, rm_7_days_before, update_base_convert_data


@shared_task
def update_base_convert():
    update_base_convert_data()


@shared_task
def update_base_convert_close_price():
    update_base_convert_data(is_save_file=True)


@shared_task
def rm_7days_before():
    rmd_filenames = get_7_days_before()
    rm_7_days_before(rmd_filenames)
    print('execute rm_7days_before()..')
