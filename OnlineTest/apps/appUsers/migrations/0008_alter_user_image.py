# Generated by Django 4.0.1 on 2022-04-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0007_rename_adress_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.png', max_length=255, upload_to='img/users_ico', verbose_name='头像'),
        ),
    ]