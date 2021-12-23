from datetime import datetime

from django.db import models

from utils.common import upload_path_handler


class ImageFile(models.Model):

    INST_TYPE = (
        ('0', 'unknown'),
        ('2', 'topic'), # 树洞 / 表白墙 / 卖舍友
        ('3', 'idle'),
        ('4', 'avatar'),
    )

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

    inst_type = models.CharField(max_length=4, choices=INST_TYPE, verbose_name='图片类型', default='0', db_index=True)
    inst_id = models.CharField(verbose_name='类型实例ID', default='0', max_length=128)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, null=True, blank=True,
                              db_index=True)
    file_path = models.FileField(upload_to=upload_path_handler(), verbose_name='图片', help_text='图片（ImageField）', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）',auto_now_add=True, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)

    def __str__(self):
        return self.file_path


    class Meta:
        db_table = 'image_file'
        verbose_name = '图片文件'
        verbose_name_plural = verbose_name
