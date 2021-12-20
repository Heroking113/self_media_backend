import ast

import requests
from celery import shared_task
from django.conf import settings

from utils.redis_cli import redisCli

APP_ID = settings.SCH_ID_SECRET[2]['APP_ID']
APP_SECRET = settings.SCH_ID_SECRET[2]['APP_SECRET']


@shared_task
def fetch_access_token():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + APP_ID + '&secret=' + APP_SECRET
    res = requests.get(url=url, headers=headers, verify=False).text
    res = ast.literal_eval(res)
    access_token = res.get('access_token', '')
    redisCli.set(key='access_token', value=access_token, ex=6600)
    return access_token