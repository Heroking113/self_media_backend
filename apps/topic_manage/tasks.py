from __future__ import absolute_import

import os
import re
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.conf import settings

from apps.topic_manage.models import TopicManage


@shared_task
def clean_up_topic_view_uids():
    with transaction.atomic():
        TopicManage.objects.select_for_update().all().update(view_uids='')

@shared_task
def async_del_topic(inst_id, img_paths):
    media_root = settings.MEDIA_ROOT
    with transaction.atomic():
        for path in img_paths:
            img_abs_path = media_root + path.split('media')[1]
            os.remove(img_abs_path)
        TopicManage.objects.select_for_update().filter(id=inst_id).delete()
