import json

from tencentcloud.ocr.v20181119 import ocr_client, models
from tencentcloud.common import credential
from tencentcloud.common.exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.asr.v20190614 import asr_client, models
from tencentcloud.ft.v20200304 import ft_client, models

from utils.common import encode_file_to_base64st
from utils.exceptions import HTTP_497_REQUEST_SIZE_LIMIT_EXCEEDED, HTTP_493_CONVERT_FAIL

TENCENT_SECRET_ID = 'AKIDKRHrADzUheJhoeEWXHkxwf7IDsIRJuKT'
TENCENT_SECRET_KEY = 'tVquhDSR9bmhMkskNkqgFXYR8ZkeHdhU'

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def tencent_ocr(img_path):
    try:
        cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = 'ocr.tencentcloudapi.com'

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, 'ap-guangzhou', clientProfile)
        req = models.GeneralAccurateOCRRequest()
        buffer = encode_file_to_base64st(img_path)
        req.ImageBase64 = buffer
        return client.GeneralAccurateOCR(req).TextDetections

    except TencentCloudSDKException as err:
        raise HTTP_497_REQUEST_SIZE_LIMIT_EXCEEDED('图片太大')


def get_sentence_recognition(mp3_file_path):

    """
    接口文档：https://console.cloud.tencent.com/api/explorer?Product=asr&Version=2019-06-14&Action=SentenceRecognition
    """
    try:
        cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = 'asr.tencentcloudapi.com'

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, '', clientProfile)

        req = models.SentenceRecognitionRequest()

        base_data = encode_file_to_base64st(mp3_file_path)
        params = {
            'ProjectId': 0,
            'SubServiceType': 2,
            'EngSerViceType': '16k_zh',  # 普通话：16k_zh; 粤语：16k_ca
            'SourceType': 1,
            'VoiceFormat': 'mp3',
            'UsrAudioKey': '123456789',
            'Data': base_data,
            'FilterDirty': 2
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentenceRecognition(req)
        return resp.Result

    except TencentCloudSDKException as err:
        return {'errMsg': 'fail'}


def face_gender_convert(to_gender, img_buffer, img_url=''):
    """
    人脸性别变换
    0：男转女
    1：女转男
    """
    try:
        cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ft.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ft_client.FtClient(cred, "ap-guangzhou", clientProfile)

        req = models.SwapGenderPicRequest()
        params = {
            "Image": img_buffer,
            "Url": img_url,
            "GenderInfos": [
                {
                    "Gender": to_gender
                }
            ],
            "RspImgType": "url"
        }
        req.from_json_string(json.dumps(params))
        resp = client.SwapGenderPic(req)
        ret = resp.to_json_string()
        return json.loads(ret)['ResultUrl']
    except TencentCloudSDKException as err:
        raise HTTP_493_CONVERT_FAIL(err.message)


def img_animation():
    """图片动漫化"""

    import json
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.ft.v20200304 import ft_client, models
    try:
        cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ft.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ft_client.FtClient(cred, "ap-guangzhou", clientProfile)

        req = models.FaceCartoonPicRequest()
        params = {
            "Url": "https://www.xizhengmy.cn/media/tmp/IMG_20170712_000926.jpg",
            "RspImgType": "url"
        }
        req.from_json_string(json.dumps(params))

        resp = client.FaceCartoonPic(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)