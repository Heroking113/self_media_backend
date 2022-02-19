from __future__ import absolute_import

import os
import re
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.conf import settings
from django.db.models import Q

from apps.topic_manage.models import TopicManage, CommentManage


@shared_task
def clean_up_topic_view_ids():
    with transaction.atomic():
        TopicManage.objects.select_for_update().all().update(view_ids='')
