# Generated by Django 4.0.1 on 2022-03-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0005_user_erp_no_user_hr_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='self_index',
            field=models.CharField(default='', max_length=100, verbose_name='定制主页'),
        ),
    ]
