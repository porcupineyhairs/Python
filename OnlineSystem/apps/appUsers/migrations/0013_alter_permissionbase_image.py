# Generated by Django 4.0.1 on 2022-04-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0012_permissionbase_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionbase',
            name='image',
            field=models.CharField(default='fa-tasks', max_length=100, verbose_name='图标'),
        ),
    ]
