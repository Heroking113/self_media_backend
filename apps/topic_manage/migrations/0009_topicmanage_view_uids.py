# Generated by Django 3.2.3 on 2021-12-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic_manage', '0008_alter_topicmanage_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicmanage',
            name='view_uids',
            field=models.TextField(blank=True, null=True, verbose_name='浏览的用户id'),
        ),
    ]
