# Generated by Django 3.2.3 on 2022-01-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage', '0023_alter_imagefile_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='file_path',
            field=models.FileField(blank=True, help_text='图片（ImageField）', null=True, upload_to='photos/2022-01-15', verbose_name='图片'),
        ),
    ]
