import json

from celery import shared_task
from django.db import transaction

from apps.topic_manage.models import TopicManage, CommentManage
from apps.user_manage.models import SchUserManage
from utils.common import change_img_size
from utils.wx_util import wx_img_sec_check


@shared_task
def async_img_sec_check(img_list):
    img_list = json.loads(img_list)
    for item in img_list:
        file_path = item['file_path']
        buffer = change_img_size(file_path)
        wx_img_sec_check(buffer, item)