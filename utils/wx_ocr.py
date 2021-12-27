from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

from utils.common import encode_pic_to_base64st
from utils.exceptions import HTTP_497_REQUEST_SIZE_LIMIT_EXCEEDED

TENCENT_SECRET_ID = 'AKIDKRHrADzUheJhoeEWXHkxwf7IDsIRJuKT'
TENCENT_SECRET_KEY = 'tVquhDSR9bmhMkskNkqgFXYR8ZkeHdhU'

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def tencent_ocr(img_path):
    try:
        cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)
        req = models.GeneralAccurateOCRRequest()
        buffer = encode_pic_to_base64st(img_path)
        req.ImageBase64 = buffer
        return client.GeneralAccurateOCR(req).TextDetections

    except TencentCloudSDKException as err:
        raise HTTP_497_REQUEST_SIZE_LIMIT_EXCEEDED('图片太大')
