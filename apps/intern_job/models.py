from django.db import models

# Create your models here.
class JobManage(models.Model):

    JOB_TYPE = (
        ('0', 'unknown'),
        ('1', '兼职'),
        ('2', '实习'),
        ('3', '校招')
    )

    SCHOOL = (
        ('0', 'unknown'),
    )

    uid = models.CharField(verbose_name='用户ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    phone = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号', max_length=128, blank=True, null=True)
    email = models.CharField(verbose_name='邮箱', max_length=128, blank=True, null=True)
    job_name = models.CharField(verbose_name='岗位名称', max_length=128, default='')
    content = models.TextField(verbose_name='岗位描述', default='')
    salary = models.CharField(verbose_name='薪资', max_length=128, default='')
    job_type = models.CharField(verbose_name='工作类型', max_length=8, default='0', choices=JOB_TYPE, db_index=True)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, db_index=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    deleter_uid = models.CharField(verbose_name='下架该数据的uid', max_length=16, default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'intern_job'
        verbose_name_plural = verbose_name = '工作管理'