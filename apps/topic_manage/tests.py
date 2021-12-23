# import os
#
#
# if __name__ == '__main__':
#
#     root_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/tmp_avatars/'
#     files = os.listdir(root_path)
#     for f in files:
#         print(f)
#

import shutil
import random
import time
from datetime import datetime



def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)

def randomDate(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(frmt, time.localtime(strTimeProp(start, end, random.random(), frmt)))

#复制文件
if __name__ == '__main__':
    # ini_file = '/Users/heroking/Documents/convertible_bond/cb_backend/apps/topic_manage/urls.py'
    # tar_file = '/Users/heroking/Documents/convertible_bond/cb_backend/apps/topic_manage/urls_des.py'
    # shutil.copyfile(ini_file, tar_file)
    start = '2021-12-23 08:00:00'
    end = '2021-12-24 02:00:00'
    ra_time = randomDate(start, end)
    da_time = datetime.strptime(ra_time, '%Y-%m-%d %H:%M:%S')
    print(ra_time, type(ra_time), da_time, type(da_time))
#复制目录
# shutil.copytree(d:/www, c:/temp/)