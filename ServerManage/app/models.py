from django.db import models
import django.utils.timezone as timezone
import os
# Create your models here.
from django.contrib.auth.models import User


# DataTable Class
# 程序信息明细
class Program(models.Model):
	id = models.AutoField(primary_key=True)
	create_date = models.DateTimeField('创建日期', default=timezone.now)
	system_name = models.CharField(max_length=50)
	prog_name = models.CharField(max_length=100)
	remark = models.CharField(max_length=255)


class OptionType(models.Model):
	id = models.AutoField(primary_key=True)
	option_name = models.CharField(max_length=50)
	

class LoginLog(models.Model):
	id = models.AutoField(primary_key=True)
	create_date = models.DateTimeField('创建日期', default=timezone.now)
	userid = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	log_type = models.CharField(max_length=50)


class OptionLog(models.Model):
	id = models.AutoField(primary_key=True)
	create_date = models.DateTimeField('创建日期', default=timezone.now)
	prog_id = models.CharField(max_length=50)
	prog_name = models.CharField(max_length=50)
	system_name = models.CharField(max_length=50)
	option_name = models.CharField(max_length=50)
	remark = models.CharField(max_length=255)
