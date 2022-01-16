import json
import os

from celery import shared_task
from django.conf import settings
from django.db import transaction

from apps.file_manage.models import AudioFile
from utils.common import change_img_size
from utils.wx_util import wx_img_sec_check


@shared_task
def async_img_sec_check(img_list):
    img_list = json.loads(img_list)
    for item in img_list:
        file_path = item['file_path']
        school = item['school']
        buffer = change_img_size(file_path)
        wx_img_sec_check(school, buffer, item)


@shared_task
def async_del_audio_info(audio_id, audio_path):
    with transaction.atomic():
        os.remove(audio_path)
        AudioFile.objects.select_for_update().filter(id=audio_id).delete()
