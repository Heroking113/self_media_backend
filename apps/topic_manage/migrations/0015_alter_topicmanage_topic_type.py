# Generated by Django 3.2.3 on 2022-02-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic_manage', '0014_topicmanage_is_top'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmanage',
            name='topic_type',
            field=models.CharField(blank=True, choices=[('0', 'unknown'), ('1', 'mood'), ('2', 'confession'), ('3', 'sellmate')], db_index=True, default='0', max_length=8, null=True, verbose_name='帖子类型'),
        ),
    ]
