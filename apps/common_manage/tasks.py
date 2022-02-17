import os

from celery import shared_task
from django.conf import settings
from django.db import transaction

from apps.idle.models import IdleManage
from apps.intern_job.models import JobManage
from apps.topic_manage.models import TopicManage, CommentManage
from apps.user_manage.models import SchUserManage
from utils.redis_cli import redisCli

from utils.wx_util import fetch_sch_access_token


@shared_task
def fetch_sch_all_access_token():
    SCH_ID_SECRET = settings.SCH_ID_SECRET
    for index, item in enumerate(SCH_ID_SECRET):
        if item and item['APP_ID'] and item['APP_SECRET']:
            access_token = fetch_sch_access_token(item['APP_ID'], item['APP_SECRET'])
            key = 'access_token_' + str(index)
            redisCli.set(key=key, value=access_token, ex=6600)


@shared_task
def update_user_profile(params, is_update_userprofile=True):
    print('update_user_profile')
    user_params = {}

    if 'avatar_url' in params:
        user_params.update({'avatar_url': params['avatar_url']})
    if 'nickname' in params:
        user_params.update({'nickname': params['nickname']})

    with transaction.atomic():
        if is_update_userprofile:
            # 更新用户信息
            SchUserManage.objects.select_for_update().filter(uid=params['uid']).update(**user_params)

        # 更新闲置相关用户信息
        IdleManage.objects.select_for_update().filter(uid=params['uid']).update(**user_params)
        # 更新招聘相关用户信息
        JobManage.objects.select_for_update().filter(uid=params['uid']).update(**user_params)
        # 更新topic相关用户信息
        TopicManage.objects.select_for_update().filter(uid=params['uid']).update(**user_params)
        # 更新评论相关用户信息
        if 'nickname' in params:
            CommentManage.objects.select_for_update().filter(uid=params['uid']).update(nickname=params['nickname'])
            CommentManage.objects.select_for_update().filter(fir_comment_uid=params['uid']).update(fir_comment_nickname=params['nickname'])


@shared_task
def async_del_tmp_funny_imgs(img_paths):
    for path in img_paths:
        os.remove(path)