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
