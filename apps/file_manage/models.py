from datetime import datetime

from django.db import models

from utils.common import upload_path_handler


class ImageFile(models.Model):

    INST_TYPE = (
        ('0', 'unknown'),
    )

    SCHOOL = (
        ('0', 'unknown'),
    )

    inst_type = models.CharField(max_length=4, choices=INST_TYPE, verbose_name='图片类型', default='0', db_index=True)
    inst_id = models.CharField(verbose_name='类型实例ID', default='0', max_length=128)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, null=True, blank=True,
                              db_index=True)
    file_path = models.FileField(upload_to=upload_path_handler(), verbose_name='图片', help_text='图片（ImageField）', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)

    def __str__(self):
        return self.file_path

    class Meta:
        db_table = 'image_file'
        verbose_name = '图片管理'
        verbose_name_plural = verbose_name
