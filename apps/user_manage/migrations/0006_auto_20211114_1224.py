# Generated by Django 3.1 on 2021-11-14 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0005_auto_20211109_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermanage',
            name='gender',
            field=models.CharField(choices=[('0', 'unknown'), ('1', '男'), ('2', '女')], default='0', max_length=16, verbose_name='性别'),
        ),
    ]
