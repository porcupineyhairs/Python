# Generated by Django 4.0.1 on 2022-03-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0002_rename_dept_id_user_dept_rename_group_id_user_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.CharField(default='', max_length=5000, verbose_name='用户权限'),
        ),
    ]
