import requests
import logging
import json

USERNAME = 'heroking'
PASSWORD = 'Heroking113.'

logger = logging.getLogger('cb_backend')


def user_login():
    url = 'http://auth.z3cloud.cn/sign/in'
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    resp = requests.post(url, data)
    if resp.status_code == 200:
        return json.loads(resp.content.decode('UTF-8'))
    logger.error('调用数据中心api报错，url is: {}'.format(url))


def get_interface_token(user_token):
    url = 'http://auth.z3cloud.cn/base/FACTOR_VOLAT'
    headers = {'Authorization': 'bearer ' + user_token}
    data = {'api': 'FACTOR_VOLAT'}
    resp = requests.post(url=url, headers=headers, data=data)
    return resp


if __name__ == '__main__':
    # u_ret = user_login()
    # user_token = u_ret['data']['token']
    # get_interface_token(user_token)
    pass