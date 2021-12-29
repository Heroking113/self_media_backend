from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery, platforms
from celery.schedules import crontab


# 把置默认的django settings模块配置给celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cb_backend.settings')
app = Celery('cb_backend')

# 这里使用字符串以使celery的worker不用为子进程序列化配置对象。
# 命名空间 namespace='CELERY'定义所有与celery相关的配置的键名要以'CELERY_'为前缀。
app.config_from_object('django.conf:settings', namespace='CELERY')

# 时区
app.conf.enable_utc = True
app.conf.timezone = "Asia/Shanghai"

# 从所有django app configs中加载task模块，
# 如果你把所有的task都定义在单独的tasks.py模块中，
# 加上这句话celery会自动发现这些模块中的task，实际上这句话可以省略。
app.autodiscover_tasks()

"""
后台定时任务：
- 刷新基础的可转债数据：
  - 每天10:00，12:00，14:00，仅刷新数据到mysql和redis
  - 每天15:10，刷新数据到mysql和redis，同时存储数据到本地
- 删除7天前的可转债基础数据文件：每天0：00处理
- 统计持有总资产：每天15:15统计一遍
- 统计持有总盈亏：每天15:15统计一遍
- 统计每支可转债盈亏：每天15:15统计一遍
- 每小时更新一次access_token

"""
# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

# 定时任务配置
app.conf.update(
    CELERY_BEAT_SCHEDULE = {
        'update_base_convert': {
            'task': 'apps.base_convert.tasks.update_base_convert',
            'schedule': crontab(minute=0, hour='10,12,14')
        },
        'update_base_convert_close_price': {
            'task': 'apps.base_convert.tasks.update_base_convert_close_price',
            'schedule': crontab(minute=10, hour=15),
        },
        'rm_7days_before': {
            'task': 'apps.base_convert.tasks.rm_7days_before',
            'schedule': crontab(minute=0, hour=0, day_of_week=1),
        },
        'statistic_asset_pl': {
            'task': 'apps.user_manage.tasks.statistic_asset_pl',
            'schedule': crontab(minute=15, hour=15)
        },
        'statistic_day_bond_pl': {
            'task': 'apps.bond_manage.tasks.statistic_day_bond_pl',
            'schedule': crontab(minute=15, hour=15)
        },
        'fetch_sch_all_access_token': {
            'task': 'apps.common_manage.tasks.fetch_sch_all_access_token',
            'schedule': crontab(minute=0, hour='*')
        },
        'clean_up_topic_view_uids': {
            'task': 'apps.topic_manage.tasks.clean_up_topic_view_uids',
            'schedule': crontab(minute=0, hour=0)
        },
        'rm_redundant_cards': {
            'task': 'apps.user_manage.tasks.rm_redundant_cards',
            'schedule': crontab(minute=0, hour=3)
        }
    }
)
