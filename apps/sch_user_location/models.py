from django.db import models


class Location(models.Model):

    SCHOOL = (
        ('0', 'unknown'),
        ('1', '深圳大学'),
        ('2', '暨南大学深圳校区'),
        ('3', '南方科技大学'),
        ('4', '哈尔滨工业大学'),
        ('5', '香港中文大学'),
        ('6', '深圳职业技术学院'),
        ('7', '深圳信息职业技术学院'),
        ('8', '中山大学'),
        ('9', '深圳理工大学'),
        ('10', '北理莫斯科大学'),
        ('11', '深圳技师学院')
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
