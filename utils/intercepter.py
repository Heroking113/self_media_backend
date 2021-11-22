# 自定义异常处理
import logging

from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status

logger = logging.getLogger('cb_backend')


def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    if response is None:
        return Response({
            'errmsg': 'server error: {exc}'.format(exc=exc),
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'exception': True
        })

    return Response({
        'errmsg': '{exc}'.format(exc=exc),
        'status_code': response.status_code,
        'exception': True
    })
