# Generated by Django 3.2.3 on 2021-12-27 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0016_alter_schusermanage_authenticate_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schusermanage',
            name='school_card',
            field=models.FileField(blank=True, null=True, upload_to='school_card/2021-12-27', verbose_name='学生校卡'),
        ),
    ]
