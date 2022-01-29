import json

from celery import shared_task
from utils.common import change_img_size
from utils.wx_util import wx_img_sec_check


@shared_task
def async_img_sec_check(img_list):
    for item in img_list:
        file_path = item['file_path']
        school = item['school']
        buffer = change_img_size(file_path)
        wx_img_sec_check(school, buffer, item)
