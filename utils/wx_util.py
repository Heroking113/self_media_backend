# -*- coding: utf-8 -*-

import json

import requests
import logging
from django.conf import settings
from django.db import transaction

from apps.common_manage.tasks import fetch_access_token
from apps.file_manage.models import ImageFile
from apps.idle_manage.models import IdleManage
from apps.topic_manage.models import TopicManage
from utils.common import send_email
from utils.exceptions import GET_SESSION_KEY_OPENID_FAIL_598
from utils.redis_cli import redisCli

logger = logging.getLogger('cb_backend')


def get_openid_session_key_by_code(js_code, app_id, app_secret):

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + app_id + '&js_code=' + js_code + '&grant_type=authorization_code' + '&secret=' + app_secret
    try:
        response = requests.get(url=url)
    except Exception:
        err_msg = 'fail to get session_key and openid.'
        logger.error(err_msg)
        raise GET_SESSION_KEY_OPENID_FAIL_598(err_msg)

    if response.status_code == 200:
        ret = eval(str(response.content, encoding="utf-8"))
        if ret.__contains__('errmsg') and 'invalid code' in ret['errmsg']:
            logger.error(ret['errmsg'])
            raise GET_SESSION_KEY_OPENID_FAIL_598(ret['errmsg'])
        return ret
    err_msg = 'fail to get session_key and openid.'
    logger.error(err_msg)
    raise GET_SESSION_KEY_OPENID_FAIL_598(err_msg)


def wx_img_sec_check(buffer, inst_info):
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    data = {'media': ('image/png', buffer)}
    access_token = redisCli.get('access_token') or ''
    if not access_token:
        access_token = fetch_access_token()
    url = 'https://api.weixin.qq.com/wxa/img_sec_check?access_token=' + access_token
    res = requests.post(url=url, headers=headers, files=data)
    if res.status_code == 200:
        ret = json.loads(res.text)
        # 违规:
        # 1、软删除该条信息；
        # 2、邮箱通知管理员（1819785416@qq.com），由管理员通知客服联系发布者处理
        type_display = ''
        if ret.get('errcode', 0) == 87014:
            with transaction.atomic():
                """
                    软删除内容
                    邮箱通知我
                """
                if inst_info['inst_type'] == '2':
                    TopicManage.objects.select_for_update().filter(id=inst_info['inst_id']).update(is_deleted=True)
                    type_display = '帖子'
                if inst_info['inst_type'] == '3':
                    IdleManage.objects.select_for_update().filter(id=inst_info['inst_id']).update(is_deleted=True)
                    type_display = '闲置'

            # 发送邮件
            title = '有违规图片'
            up_content = '类型:{type_display}, id:{inst_id}, school:{school}'.format(type_display=type_display,
                                                                                   inst_id=inst_info['inst_id'],
                                                                                   school=inst_info['school'])
            send_email(title, up_content)


def wx_msg_sec_check(buffer, inst_info):
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    data = {
        'version': 2,
        'scene': 3,

    }
    access_token = redisCli.get('access_token') or ''
    if not access_token:
        access_token = fetch_access_token()
    url = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token=' + access_token
    res = requests.post(url=url, headers=headers, files=data)
    if res.status_code == 200:
        ret = json.loads(res.text)
        # 违规:
        # 1、软删除该条信息；
        # 2、邮箱通知管理员（1819785416@qq.com），由管理员通知客服联系发布者处理
        type_display = ''
        if ret.get('errcode', 0) == 87014:
            with transaction.atomic():
                """
                    软删除内容
                    邮箱通知我
                """
                if inst_info['inst_type'] == '2':
                    TopicManage.objects.select_for_update().filter(id=inst_info['inst_id']).update(is_deleted=True)
                    type_display = '帖子'
                if inst_info['inst_type'] == '3':
                    IdleManage.objects.select_for_update().filter(id=inst_info['inst_id']).update(is_deleted=True)
                    type_display = '闲置'

            # 发送邮件
            title = '有违规图片'
            up_content = '类型:{type_display}, id:{inst_id}, school:{school}'.format(type_display=type_display,
                                                                                   inst_id=inst_info['inst_id'],
                                                                                   school=inst_info['school'])
            send_email(title, up_content)

