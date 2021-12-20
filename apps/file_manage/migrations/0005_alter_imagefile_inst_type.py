# Generated by Django 3.2.3 on 2021-12-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage', '0004_auto_20211217_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='inst_type',
            field=models.CharField(choices=[('0', 'unknown'), ('1', 'swiper'), ('2', 'mood'), ('3', 'confession_wall'), ('4', 'sell_roommate'), ('5', 'idle')], db_index=True, default='0', max_length=4, verbose_name='图片类型'),
        ),
    ]
