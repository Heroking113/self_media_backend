# Generated by Django 3.2.3 on 2022-01-25 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0027_alter_schusermanage_authenticate_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schusermanage',
            name='authenticate_status',
            field=models.CharField(choices=[('1', '初次登录'), ('2', '定位采集中'), ('3', '人工审核中'), ('4', '非本校用户'), ('5', '本校用户')], default='1', max_length=8, verbose_name='认证状态'),
        ),
    ]
