from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


class User(AbstractUser):
	gender_choices = (('male', '男'), ('female', '女'), ('null', '未填写'))
	
	username = models.CharField('用户名称', null=False, max_length=50, primary_key=True)
	deptid = models.IntegerField('部门编号', null=True, blank=True)
	groupname = models.IntegerField('用户组名', null=True, blank=True)
	nick_name = models.CharField('昵称', null=True, max_length=50, default='')
	birthday = models.DateField('生日', null=True, blank=True)
	gender = models.CharField('性别', max_length=10, choices=gender_choices, default='null')
	adress = models.CharField('地址', max_length=100, default='')
	mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
	email = models.EmailField('邮箱', max_length=50, null=False, default='')
	image = models.ImageField('头像', upload_to='image/%Y%m', default='image/default.png', max_length=255)
	
	dingtalkid = models.CharField('钉钉号', null=False, default='', max_length=255)
	is_dingtalk = models.BooleanField('能否钉钉登录', null=False, default=0)
	wechatid = models.CharField('微信号', null=False, default='', max_length=255)
	is_wechat = models.BooleanField('能否微信登录', null=False, default=0)
	
	first_name = models.CharField(null=True, max_length=50, default='')
	last_name = models.CharField(null=True, max_length=50, default='')
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username
	

class UserGroup(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)
	
	class Meta:
		verbose_name = '用户组'
		verbose_name_plural = verbose_name
	 

class Department(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	manageuser = models.CharField(max_length=50)
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)
	
	class Meta:
		verbose_name = '部门信息'
		verbose_name_plural = verbose_name


class PermissionBase(models.Model):
	id = models.AutoField(primary_key=True)
	valid = models.BooleanField('有效值', null=False, default=True)
	parent = models.IntegerField('父权限ID', null=False, default=0)
	name = models.CharField('权限名', null=False, max_length=50)
	url = models.CharField('URL地址', null=False, max_length=100, default='')
	show_index = models.IntegerField('显示排序', null=False, default=99)
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)
	
	class Meta:
		verbose_name = '权限基础表'
		verbose_name_plural = verbose_name
	pass


class PermissionGroup(models.Model):
	id = models.AutoField(primary_key=True)
	groupname = models.CharField('权限组名', max_length=50, null=False)
	permissionid = models.IntegerField('权限id', null=False)
	permissionname = models.CharField('权限名', null=False, max_length=50)
	
	run = models.BooleanField(null=False, default=0)
	new = models.BooleanField(null=False, default=0)
	edit = models.BooleanField(null=False, default=0)
	delete = models.BooleanField(null=False, default=0)
	print = models.BooleanField(null=False, default=0)
	output = models.BooleanField(null=False, default=0)
	lock = models.BooleanField(null=False, default=0)
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)
	
	class Meta:
		verbose_name = '组权限'
		verbose_name_plural = verbose_name
		

class PermissionUser(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField('用户名', max_length=50, null=False)
	permissionid = models.IntegerField('权限id', null=False)
	permissionname = models.CharField('权限名', null=False, max_length=50)
	
	run = models.BooleanField(null=False, default=0)
	new = models.BooleanField(null=False, default=0)
	edit = models.BooleanField(null=False, default=0)
	delete = models.BooleanField(null=False, default=0)
	print = models.BooleanField(null=False, default=0)
	output = models.BooleanField(null=False, default=0)
	lock = models.BooleanField(null=False, default=0)
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=True, default=timezone.now)
	createuser = models.CharField('创建人', null=True, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True)
	modiuser = models.CharField('创建人', null=True, max_length=50)
	
	class Meta:
		verbose_name = '用户权限'
		verbose_name_plural = verbose_name
