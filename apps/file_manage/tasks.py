import json

from celery import shared_task

from utils.common import change_img_size


# @shared_task
# def async_img_sec_check(img_list):
#     img_list = json.loads(img_list)
#     for item in img_list:
#         file_path = item['file_path']
#         buffer = change_img_size(file_path)
        # wx_img_sec_check(buffer, item)