# Generated by Django 3.2.3 on 2021-12-23 00:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('topic_manage', '0006_alter_topicmanage_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmanage',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='创建的时间', verbose_name='创建的时间'),
        ),
    ]
