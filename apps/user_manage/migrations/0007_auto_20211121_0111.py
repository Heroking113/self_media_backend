# Generated by Django 3.1 on 2021-11-21 01:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0006_auto_20211114_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetmanage',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assetmanage',
            name='held_assets',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13, verbose_name='持有资产'),
        ),
    ]
