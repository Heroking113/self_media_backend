# Generated by Django 3.2.3 on 2021-12-27 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage', '0018_alter_imagefile_inst_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='inst_type',
            field=models.CharField(choices=[('0', 'unknown'), ('2', 'topic'), ('3', 'idle'), ('4', 'avatar')], db_index=True, default='0', max_length=4, verbose_name='图片类型'),
        ),
    ]
