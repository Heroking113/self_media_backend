# Generated by Django 3.1 on 2021-11-12 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]
