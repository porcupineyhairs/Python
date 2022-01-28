from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


class UserProfile(AbstractUser):
	gender_choices = (
		('male', '男'),
		('female', '女')
	)

	deptid = models.IntegerField(_('deptid'), blank=True)
	projectid = models.IntegerField(_('projectid'), blank=True)
	nick_name = models.CharField('昵称', max_length=50, default='')
	birthday = models.DateField('生日', null=True, blank=True)
	gender = models.CharField('性别', max_length=10, choices=gender_choices, default='female')
	adress = models.CharField('地址', max_length=100, default='')
	mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
	image = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username
	 

# 部门表——Dept
# 部门ID——deptid
# 部门名称——deptname
# 部门经理——User
class Deptd(models.Model):
	deptid = models.AutoField(primary_key=True)
	deptname = models.CharField(max_length=20)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)


# 项目管理-Project
# 项目ID——id
# 项目名称——name
# 合同金额——price
# 所属部门——Dept
# 开发工作量——day
# 缺陷数——error
# 项目描述——describe
class Project(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=80)
	price = models.IntegerField()
	deptd = models.ForeignKey(Deptd, blank=True, null=True, on_delete=models.DO_NOTHING)
	day = models.IntegerField()
	error = models.IntegerField()
	describe = models.CharField(max_length=500)


# 产品表-Product
# 产品ID——pid
# 产品名称——pname
# 产品管理员——User
# 产品描述——pdescribe
class Product(models.Model):
	pid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
	pdescribe = models.CharField(max_length=500)
	projectid = models.IntegerField(blank=True, null=True)


# 产品版本号表-Pversion
# 版本号ID-vid
# 产品ID——Product
# 发布日期——date
# 版本类型——type
# 产品版本号——vnumber
# 创建时写入日期 不改变


class Pversion(models.Model):
	vid = models.AutoField(primary_key=True)
	product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.DO_NOTHING)
	vnumber = models.CharField(max_length=10, blank=True, null=True)
	date = models.DateTimeField('保存日期', default=timezone.now)
	type = models.CharField(max_length=10)


# 产品资料管理-Means
# 资料ID——id
# 资料名称——name
# 产品ID——Product
# 产品版本号——Pversion
# 资料类型——程序/样例代码/文档-type
# 资料——filepath
# 资料说明——explain
class Means(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.DO_NOTHING)
	pversion = models.ForeignKey(Pversion, blank=True, null=True, on_delete=models.DO_NOTHING)
	type = models.CharField(max_length=10)
	filepath = models.CharField(max_length=200)
	explain = models.CharField(max_length=500)


# 产品问题管理-Matter
# 问题ID——mid
# 问题标题——mtitle
# 产品ID——pid
# 产品版本号ID——Pversion
# 产品模块——model
# 严重程度——1-5越大越严重-extent
# 要求解决日期——solvedate
# 问题描述——describe
# 提出项目组——proid
# 问题提交日期——mdate
# 问题提交人——quid
# 问题状态——待分配/已分配/已解决/已确认-state
# 解决人——ruid
# 消缺版本号——nvnumber
# 解决说明——mexplain
# 实际解决日期——sdate
# 确认日期——qdate
class Matter(models.Model):
	mid = models.AutoField(primary_key=True)
	mtitle = models.CharField(max_length=150)
	pid = models.IntegerField()
	pversion = models.ForeignKey(Pversion, blank=True, null=True, on_delete=models.DO_NOTHING)
	model = models.CharField(max_length=60)
	extent = models.IntegerField()
	solvedate = models.DateField()
	describe = models.CharField(max_length=200)
	proid = models.IntegerField()
	mdate = models.DateTimeField('保存日期', default=timezone.now)
	quid = models.IntegerField()
	state = models.CharField(max_length=10)
	ruid = models.IntegerField(blank=True, null=True)
	nvnumber = models.IntegerField(blank=True, null=True)
	mexplain = models.CharField(max_length=200, blank=True, null=True)
	sdate = models.DateTimeField(blank=True, null=True)
	qdate = models.DateTimeField(blank=True, null=True)


class Dongtai(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=80, blank=True, null=True)
	describe = models.CharField(max_length=200)
	date = models.DateTimeField('保存日期', default=timezone.now)
