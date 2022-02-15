# Generated by Django 3.2.3 on 2022-02-15 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idle', '0003_idlemanage_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idlemanage',
            name='content',
            field=models.TextField(default='', verbose_name='闲置描述'),
        ),
        migrations.AlterField(
            model_name='idlemanage',
            name='idle_type',
            field=models.CharField(choices=[('0', 'unknown'), ('1', '生活用品'), ('2', '学习用品')], default='0', max_length=8, verbose_name='闲置类型'),
        ),
    ]
