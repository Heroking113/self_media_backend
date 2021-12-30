# -*- coding: utf-8 -*-

import json
import ast
import requests
import logging
from django.conf import settings
from django.db import transaction

from apps.idle_manage.models import IdleManage
from apps.topic_manage.models import TopicManage
from utils.exceptions import GET_SESSION_KEY_OPENID_FAIL_598, HTTP_495_IMG_SENSITIVE
from utils.redis_cli import redisCli

logger = logging.getLogger('cb_backend')


def fetch_sch_access_token(APP_ID, APP_SECRET, reset=False, sch_index=0):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + APP_ID + '&secret=' + APP_SECRET
    res = requests.get(url=url, headers=headers, verify=False).text
    res = ast.literal_eval(res)
    access_token = res.get('access_token', '')
    if reset:
        key = 'access_token_' + str(sch_index)
        redisCli.set(key=key, value=access_token, ex=6600)
    return access_token



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


def wx_img_sec_check(school, buffer, inst_info):
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    data = {'media': ('image/png', buffer)}
    key = 'access_token_' + str(school)
    access_token = redisCli.get(key) or ''
    if not access_token:
        school = int(school)
        id_secret = settings.SCH_ID_SECRET[school]
        APP_ID = id_secret['APP_ID']
        APP_SECRET = id_secret['APP_SECRET']
        access_token = fetch_sch_access_token(APP_ID, APP_SECRET, reset=True, sch_index=school)
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
            err_msg = '图片违规: ' + str(inst_info)
            logger.warning(err_msg)
            raise HTTP_495_IMG_SENSITIVE('图片违规')
            #
            # 发送邮件
            # title = '有违规图片'
            # up_content = '类型:{type_display}, id:{inst_id}, school:{school}'.format(type_display=type_display,
            #                                                                        inst_id=inst_info['inst_id'],
            #                                                                        school=inst_info['school'])
            # send_email(title, up_content)


def wx_msg_sec_check(school, openid, content, title=''):
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    data = {
        'version': 2,
        'scene': 3,
        'openid': openid,
        'content': content,
        'title': title
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = str(data).replace("'", '"')
    key = 'access_token_' + str(school)
    access_token = redisCli.get(key) or ''
    if not access_token:
        school = int(school)
        id_secret = settings.SCH_ID_SECRET[school]
        APP_ID = id_secret['APP_ID']
        APP_SECRET = id_secret['APP_SECRET']
        access_token = fetch_sch_access_token(APP_ID, APP_SECRET, reset=True, sch_index=school)
    url = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token=' + access_token
    res = requests.post(url=url, headers=headers, data=data.encode('utf-8'))
    if res.status_code == 200:
        result = json.loads(res.text)['result']
        if result['suggest'] != 'pass':
            err_msg = '内容违规: ' + data
            logger.warning(err_msg)
        return result
    return {
        'suggest': 'pass',
        'label': 100
    }

