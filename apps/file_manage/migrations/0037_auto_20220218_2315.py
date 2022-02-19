# Generated by Django 3.2.3 on 2022-02-18 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage', '0036_alter_imagefile_file_path'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagefile',
            options={'verbose_name': '图片管理', 'verbose_name_plural': '图片管理'},
        ),
        migrations.AlterField(
            model_name='imagefile',
            name='file_path',
            field=models.FileField(blank=True, help_text='图片（ImageField）', null=True, upload_to='photos/2022-02-18', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='imagefile',
            name='inst_type',
            field=models.CharField(choices=[('0', 'unknown'), ('2', 'topic'), ('3', 'idle'), ('4', 'avatar'), ('5', 'mutual')], db_index=True, default='0', max_length=4, verbose_name='图片类型'),
        ),
    ]
