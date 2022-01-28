# Generated by Django 4.0 on 2022-01-21 06:53

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('manageuser', models.CharField(max_length=50)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '部门信息',
                'verbose_name_plural': '部门信息',
            },
        ),
        migrations.CreateModel(
            name='PermissionBase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valid', models.BooleanField(default=True, verbose_name='有效值')),
                ('parent', models.IntegerField(default=0, verbose_name='父权限ID')),
                ('name', models.CharField(max_length=50, verbose_name='权限名')),
                ('url', models.CharField(default='', max_length=100, verbose_name='URL地址')),
                ('show_index', models.IntegerField(default=99, verbose_name='显示排序')),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '权限基础表',
                'verbose_name_plural': '权限基础表',
            },
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('groupname', models.CharField(max_length=50, verbose_name='权限组名')),
                ('permissionid', models.IntegerField(verbose_name='权限id')),
                ('permissionname', models.CharField(max_length=50, verbose_name='权限名')),
                ('run', models.BooleanField(default=0)),
                ('new', models.BooleanField(default=0)),
                ('edit', models.BooleanField(default=0)),
                ('delete', models.BooleanField(default=0)),
                ('print', models.BooleanField(default=0)),
                ('output', models.BooleanField(default=0)),
                ('lock', models.BooleanField(default=0)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '组权限',
                'verbose_name_plural': '组权限',
            },
        ),
        migrations.CreateModel(
            name='PermissionUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('permissionid', models.IntegerField(verbose_name='权限id')),
                ('permissionname', models.CharField(max_length=50, verbose_name='权限名')),
                ('run', models.BooleanField(default=0)),
                ('new', models.BooleanField(default=0)),
                ('edit', models.BooleanField(default=0)),
                ('delete', models.BooleanField(default=0)),
                ('print', models.BooleanField(default=0)),
                ('output', models.BooleanField(default=0)),
                ('lock', models.BooleanField(default=0)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '用户权限',
                'verbose_name_plural': '用户权限',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='用户名称')),
                ('nick_name', models.CharField(default='', max_length=50, null=True, verbose_name='昵称')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('deptid', models.IntegerField(blank=True, null=True, verbose_name='部门编号')),
                ('groupname', models.IntegerField(null=True, blank=True, verbose_name='用户组名')),
                ('email', models.EmailField(default='', max_length=50, verbose_name='邮箱')),
                ('image', models.ImageField(default='image/default.png', max_length=255, upload_to='image/%Y%m', verbose_name='头像')),
                ('dingtalkid', models.CharField(default='', max_length=255, verbose_name='钉钉号')),
                ('is_dingtalk', models.BooleanField(default=0, verbose_name='能否钉钉登录')),
                ('wechatid', models.CharField(default='', max_length=255, verbose_name='微信号')),
                ('is_wechat', models.BooleanField(default=0, verbose_name='能否微信登录')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女'), ('null', '未填写')], default='null', max_length=10, verbose_name='性别')),
                ('adress', models.CharField(default='', max_length=100, verbose_name='地址')),
                ('first_name', models.CharField(default='', max_length=50, null=True)),
                ('last_name', models.CharField(default='', max_length=50, null=True)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('modidate', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('modiuser', models.CharField(max_length=50, null=True, verbose_name='创建人')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
