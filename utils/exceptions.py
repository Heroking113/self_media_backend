from rest_framework import status
from rest_framework.exceptions import APIException


class HTTP_404_NOT_FOUND(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class GET_SESSION_KEY_OPENID_FAIL_598(APIException):
    status_code = 598


class HTTP_499_DATA_EXIST(APIException):
    status_code = 499


class HTTP_498_NOT_IN_IP_WHITELIST(APIException):
    status_code = 498


class HTTP_497_REQUEST_SIZE_LIMIT_EXCEEDED(APIException):
    status_code = 497


class HTTP_496_MSG_SENSITIVE(APIException):
    status_code = 496


class HTTP_495_IMG_SENSITIVE(APIException):
    status_code = 495
