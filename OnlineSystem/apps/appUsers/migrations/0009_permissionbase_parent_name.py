# Generated by Django 4.0.1 on 2022-04-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0008_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionbase',
            name='parent_name',
            field=models.CharField(default='', max_length=100, verbose_name='ηΆζιε'),
        ),
    ]
