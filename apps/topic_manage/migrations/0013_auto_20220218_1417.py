# Generated by Django 3.2.3 on 2022-02-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic_manage', '0012_auto_20220218_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmanage',
            name='liker_ids',
            field=models.TextField(blank=True, default='', help_text='浏览用户的id(避免uid占用过带宽)', null=True, verbose_name='点赞用户的id'),
        ),
        migrations.AlterField(
            model_name='topicmanage',
            name='view_ids',
            field=models.TextField(blank=True, default='', help_text='浏览用户的id(避免uid占用过带宽)', null=True, verbose_name='浏览用户的id'),
        ),
    ]
