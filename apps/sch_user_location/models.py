from django.db import models


class Location(models.Model):

    SCHOOL = (
        ('0', 'unknown')
    )

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, null=True, blank=True)
    latitude = models.CharField(verbose_name='纬度', max_length=32, default='')
    longitude = models.CharField(verbose_name='经度', max_length=32, default='')
    sta_dist_one = models.IntegerField(verbose_name='与标准位置一的距离(m)', default=-1)
    sta_dist_two = models.IntegerField(verbose_name='与标准位置二的距离(m)', default=-1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'sch_location'
        verbose_name_plural = verbose_name = '高校用户定位数据管理'
