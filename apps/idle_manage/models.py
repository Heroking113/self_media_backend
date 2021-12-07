from django.db import models

# Create your models here.
class IdleManage(models.Model):
    ORDER_STATUS = (
        ('1', '售卖中'),
        ('2', '已卖出'),
        ('3', '已下架')
    )

    uid = models.CharField(verbose_name='用户对外ID', max_length=16, default='')
    nickname = models.CharField(verbose_name='卖家昵称', max_length=32, default='')
    avatar_url = models.TextField(verbose_name='卖家头像地址', default='')
    wechat = models.CharField(verbose_name='卖家微信', max_length=128, default='')
    mobile = models.CharField(verbose_name='卖家手机号', max_length=11, default='')
    title = models.CharField(max_length=32, verbose_name='物品名称', help_text='物品名称', default='')
    sell_price = models.DecimalField(verbose_name='售价', help_text='售价', max_digits=10, decimal_places=2, default=0)
    description = models.CharField(verbose_name='物品描述', help_text='物品描述', max_length=512, default='')
    img_paths = models.TextField(verbose_name='图片路由', default='')
    order_status = models.CharField(verbose_name='订单状态', help_text='订单状态', max_length=8, choices=ORDER_STATUS,
                                    default='1')
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建的时间', help_text='创建的时间', auto_now_add=True)

    class Meta:
        db_table = 'idle_manage'
        verbose_name_plural = verbose_name = '闲置管理'
