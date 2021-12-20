from django.db import models

# Create your models here.
class TopicManage(models.Model):

    TOPIC_TYPE = (
        ('0', 'unknown'),
        ('1', 'mood'),
        ('2', 'confession'),
        ('3', 'sellmate')
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
        ('10', '北理莫斯科大学')
    )

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='用户头像地址', default='')
    title = models.CharField(max_length=32, verbose_name='帖子标题', default='', null=True, blank=True)
    content = models.CharField(verbose_name='帖子内容', max_length=512, default='')
    topic_type = models.CharField(verbose_name='帖子类型', max_length=8, default='0', choices=TOPIC_TYPE, null=True, blank=True)
    school = models.CharField(verbose_name='学校', max_length=8, default='0', choices=SCHOOL, null=True, blank=True, db_index=True)
    view_count = models.IntegerField(verbose_name='浏览量', default=0)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    img_paths = models.TextField(verbose_name='图片路由', default='')
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'topic_manage'
        verbose_name_plural = verbose_name = '帖子管理'


class CommentManage(models.Model):
    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, default='')
    inst_id = models.IntegerField(verbose_name='帖子ID', default=0)
    content = models.CharField(verbose_name='评论内容', max_length=256, default='')
    is_sec_comment = models.BooleanField(verbose_name='是否二级评论', default=False, null=True, blank=True)
    fir_comment_uid = models.CharField(verbose_name='一级评论ID', max_length=16, default='', null=True, blank=True)
    fir_comment_nickname = models.CharField(verbose_name='用户昵称', max_length=32, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'comment_manage'
        verbose_name_plural = verbose_name = '评论管理'
