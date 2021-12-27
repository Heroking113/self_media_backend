# 公众号：小柚靓靓
import json
import requests

app_id = 'wxa2ebf4090d3d4851'
app_secret = 'd6349854265dfacc96baa75f67900b71'

access_token = '52_W42ba2_BCCIbJShGHl7qBVU-Bf2FKLMXb2IVr2U_gO8itaO_HhJp4PdoCWO6aVT-5GoKvqETxJcRT75z26e9nRnO59s72m_pKv2NBQRxAnn3kmBmSyy2VV3KxbihJ4KfCmKJNITbuvm3-NBZOXOdAFAGPG'

def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'.format(APPID=app_id, APPSECRET=app_secret)
    ret = requests.get(url)
    content = str(ret.content, encoding='utf-8')
    content = json.loads(content)
    return content['access_token']


def get_sucai(access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token='+access_token
    data = {
        'type': 'image',
        'offset': 0,
        'count': 20
    }
    headers = {'Content-Type': 'application/json'}
    ret = requests.post(url, headers=headers, data=json.dumps(data))
    content = str(ret.content, encoding='utf-8')
    content = json.loads(content)
    return content


def get_single_news(media_id, access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token='+access_token
    headers = {'Content-Type': 'application/json'}
    data = {
        'media_id': media_id
    }
    ret = requests.post(url, headers=headers, data=json.dumps(data))
    content = str(ret.content, encoding='utf-8')
    content = json.loads(content)
    return content


if __name__ == '__main__':
    # access_token = get_access_token()
    # content = get_sucai(access_token)
    # for item in content['item']:
    #     ret = get_single_news(item['media_id'], access_token)
    #     print(item['url'])
    print('main')

