from django.db import models

class ImageFile(models.Model):

    INST_TYPE = (
        ('0', 'unknown'),
        ('1', 'idle'),
        ('2', 'mood'),
        ('3', 'swiper')  # 轮播图长宽比 = 5 : 2
    )

    inst_type = models.CharField(max_length=4, choices=INST_TYPE, verbose_name='图片类型', default='0', db_index=True)
    inst_id = models.IntegerField(verbose_name='类型实例ID', default=0)
    file_path = models.FileField(upload_to='photos/', verbose_name='图片', help_text='图片（ImageField）', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）',auto_now_add=True, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)

    def __str__(self):
        return self.file_path


    class Meta:
        db_table = 'image_file'
        verbose_name = '图片文件'
        verbose_name_plural = verbose_name