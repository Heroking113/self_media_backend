from __future__ import absolute_import

import re
from datetime import datetime

from celery import shared_task
from django.db import transaction

from apps.topic_manage.models import TopicManage


@shared_task
def clean_up_topic_view_uids():
    with transaction.atomic():
        TopicManage.objects.select_for_update().all().update(view_uids='')