# Generated by Django 3.1 on 2021-11-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0003_auto_20211104_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmanage',
            name='uid',
            field=models.CharField(default='', max_length=16, verbose_name='用户对外的ID'),
        ),
        migrations.AlterField(
            model_name='usermanage',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='usermanage',
            name='lasted_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='usermanage',
            name='uid',
            field=models.CharField(default='', max_length=16, verbose_name='用户对外的ID'),
        ),
    ]
