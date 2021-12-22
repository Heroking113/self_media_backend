from django.db import models

# Create your models here.
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
        ('10', '北理莫斯科大学')
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
