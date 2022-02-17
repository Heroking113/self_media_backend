import json

from celery import shared_task
from utils.common import change_img_size
from utils.exceptions import HTTP_501_NET_CONGEST_ERROR
from utils.wx_util import wx_img_sec_check


@shared_task
def async_img_sec_check(img_list):
    for item in img_list:
        file_path = item['file_path']
        school = item['school']
        try:
            buffer = change_img_size(file_path)
        except:
            raise HTTP_501_NET_CONGEST_ERROR('网络阻塞，请稍后再试或联系我们')
        else:
            wx_img_sec_check(school, buffer, item)
