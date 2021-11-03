import random
import string
import time


def set_uid():
    """设置用户对外的ID"""
    rt = time.strftime("%H%M%S%MS",time.localtime(time.time()))
    t = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(9)).lower()
    return ''.join([rt[4], t, rt[5]])
