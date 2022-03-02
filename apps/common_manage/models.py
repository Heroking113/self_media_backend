from django.db import models


class Configuration(models.Model):

    OPT_VAL_ONE = (
        ('unknown', 'unknown'),
        ('open', 'open'),
        ('off', 'off')
    )

    key = models.CharField(verbose_name='配置项名称', max_length=128, default='')
    opt_val_one = models.CharField(verbose_name='可选值配置项一', max_length=64, choices=OPT_VAL_ONE, default='unknown')
    uni_val = models.TextField(verbose_name='唯一值配置项', default='')
    instruction = models.TextField(verbose_name='说明', default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'configuration'
        verbose_name_plural = verbose_name = '配置管理'


class SchSwiper(models.Model):
    """  轮播图长宽比 = 5 : 2  """
    SCHOOL = (
        ('0', 'unknown'),
    )

    SWIPER_TYPE = (
        ('1', '显示图片'),
        ('2', '显示推文'),
        ('3', '跳转小程序')
    )

    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL)
    swiper_type = models.CharField(verbose_name='类型', max_length=8, default='1', choices=SWIPER_TYPE)
    img_path = models.FileField(upload_to='swiper', verbose_name='图片', help_text='图片（ImageField）')
    mp_id = models.CharField(verbose_name='小程序ID', max_length=256, null=True, blank=True)
    tweets_url = models.TextField(verbose_name='推文链接', null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否下架', default=False)

    class Meta:
        db_table = 'sch_swiper'
        verbose_name_plural = verbose_name = '轮播图管理'
