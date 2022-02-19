# Generated by Django 3.2.3 on 2022-02-18 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idle', '0004_auto_20220215_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idlemanage',
            name='idle_type',
            field=models.CharField(choices=[('0', 'unknown'), ('1', '生活用品'), ('2', '学习用品')], db_index=True, default='0', max_length=8, verbose_name='闲置类型'),
        ),
    ]
