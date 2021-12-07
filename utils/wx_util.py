import requests
import logging
from django.conf import settings

from utils.exceptions import GET_SESSION_KEY_OPENID_FAIL_598

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
