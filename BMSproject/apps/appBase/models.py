from django.db import models
import django.utils.timezone as timezone


class AppConfig(models.Model):
	id = models.AutoField(primary_key=True)
	valid = models.BooleanField('有效值', null=False, default=True)
	apps = models.CharField('应用类别', null=False, max_length=50)
	name = models.CharField('配置名', null=False, max_length=50)
	value = models.CharField('配置值', null=False, max_length=500, default='')
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=False, default=timezone.now)
	createuser = models.CharField('创建人', null=False, max_length=50)
	modidate = models.DateTimeField('修改时间', null=True, default='')
	modiuser = models.CharField('创建人', null=True, default='', max_length=50)
	
	class Meta:
		verbose_name = '配置信息表'
		verbose_name_plural = verbose_name


class AppLog(models.Model):
	id = models.AutoField(primary_key=True)
	apps = models.CharField('应用类别', null=False, max_length=50)
	model = models.CharField('模块名', null=False, max_length=50)
	key = models.CharField('数据主键', null=False, max_length=50)
	value = models.CharField('数据值', null=False, max_length=255, default='')
	
	remark = models.CharField('备注', null=True, max_length=255)
	createdate = models.DateTimeField('创建时间', null=False, default=timezone.now)
	createuser = models.CharField('创建人', null=False, max_length=50)
	
	class Meta:
		verbose_name = '日志记录表'
		verbose_name_plural = verbose_name

