# Generated by Django 3.2.3 on 2021-12-27 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0015_schusermanage_school_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schusermanage',
            name='authenticate_status',
            field=models.CharField(choices=[('1', '未认证'), ('2', '人工审核中'), ('3', '已认证'), ('4', '认证失败')], default='1', max_length=8, verbose_name='认证状态'),
        ),
    ]
