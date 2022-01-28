from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import os, uuid
from django.contrib import messages
from app.models import Deptd, Project, Product, Pversion, Means, Matter, Dongtai

import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.global_setting import global_setting


global_setting = global_setting(None)
root_url = global_setting.get('root_url')


# 系统管理员主页
def index(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			
			aa = 0
			bb = 0
			cc = 0
			dd = 0
			eelist = Matter.objects.filter(state='待分配').count()
			
			# print(eelist)
			fflist = Matter.objects.filter(state='已分配').count()
			
			gglist = Matter.objects.filter(state='已解决').count()
			
			# print(gglist)
			hhlist = Matter.objects.filter(state='已确认').count()
			deptid = user.deptid
			xmuserlist = User.objects.filter(deptid=deptid)
			dongtailist = Dongtai.objects.all().order_by('-date')
			
			paged = Paginator(dongtailist, 8)
			try:
				page = int(request.GET.get('page', 1))
				dongtailist = paged.page(page)
			except:
				dongtailist = paged.page(1)
			
			content = {}
			content['dongtailist'] = dongtailist
			
			return render(request, 'index2.html', locals())
		elif user.last_name == '项目开发人员':
			aa = Matter.objects.filter(quid=user.id).count()
			bb = 0
			cc = 0
			cc = 0
			dd = Matter.objects.filter(state='已解决').count()
			eelist = Matter.objects.filter(state='待分配').count()
			
			# print(eelist)
			fflist = Matter.objects.filter(state='已分配').count()
			
			gglist = Matter.objects.filter(state='已解决').count()
			
			# print(gglist)
			hhlist = Matter.objects.filter(state='已确认').count()
			projextid = user.projectid
			xmuserlist = User.objects.filter(projectid=projextid)
			if projextid == 0:
				xmuserlist = [user]
			xmuserlist = User.objects.filter(projectid=projextid)
			dongtailist = Dongtai.objects.all().order_by('-date')
			paged = Paginator(dongtailist, 8)
			try:
				page = int(request.GET.get('page', 1))
				dongtailist = paged.page(page)
			except:
				dongtailist = paged.page(1)
			content = {}
			content['dongtailist'] = dongtailist
			return render(request, 'xmindex.html', locals())
		
		elif user.last_name == '产品管理员':
			aa = 0
			bb = Matter.objects.filter(state='待分配').count()
			bb2 = Matter.objects.filter(state='已分配').count()
			bb3 = Matter.objects.filter(state='已解决').count()
			bb = bb + bb2 + bb3
			cc = 0
			cc = 0
			dd = 0
			eelist = Matter.objects.filter(state='待分配').count()
			
			# print(eelist)
			fflist = Matter.objects.filter(state='已分配').count()
			
			gglist = Matter.objects.filter(state='已解决').count()
			
			# print(gglist)
			hhlist = Matter.objects.filter(state='已确认').count()
			deptid = user.deptid
			xmuserlist = User.objects.filter(deptid=deptid)
			
			dongtailist = Dongtai.objects.all().order_by('-date')
			paged = Paginator(dongtailist, 8)
			try:
				page = int(request.GET.get('page', 1))
				dongtailist = paged.page(page)
			except:
				dongtailist = paged.page(1)
			content = {}
			content['dongtailist'] = dongtailist
			return render(request, 'cpindex.html', locals())
		
		elif user.last_name == '产品开发人员':
			aa = 0
			bb = 0
			cc = Matter.objects.filter(ruid=user.id).count()
			
			dd = 0
			eelist = Matter.objects.filter(state='待分配').count()
			
			# print(eelist)
			fflist = Matter.objects.filter(state='已分配').count()
			
			gglist = Matter.objects.filter(state='已解决').count()
			
			# print(gglist)
			hhlist = Matter.objects.filter(state='已确认').count()
			projextid = user.projectid
			xmuserlist = User.objects.filter(projectid=projextid)
			if projextid == 0:
				xmuserlist = [user]
			xmuserlist = User.objects.filter(projectid=projextid)
			dongtailist = Dongtai.objects.all().order_by('-date')
			paged = Paginator(dongtailist, 8)
			try:
				page = int(request.GET.get('page', 1))
				dongtailist = paged.page(page)
			except:
				dongtailist = paged.page(1)
			
			content = {}
			content['dongtailist'] = dongtailist
			return render(request, 'kfindex.html', locals())
	
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def souname(request):
	user = request.user
	if user.is_authenticated:
		sousuo = request.POST.get('sousuode')
		print(sousuo)
		userlist = User.objects.all()
		userd = []
		for uu in userlist:
			if sousuo in uu.first_name:
				userd.append(uu)
		userlist = userd
		projuctlist = Project.objects.all()
		deptdlist = Deptd.objects.all()
		paged = Paginator(userlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			userlist = paged.page(page)
		except:
			userlist = paged.page(1)
		
		content = {}
		content['userlist'] = userlist
		jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
		if user.last_name == '系统管理员':
			return render(request, 'showuser.html', locals())
		else:
			return render(request, 'jshowuser.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 项目管理员主页
def xmindex(request):
	return render(request, 'xmindex.html')


# 产品管理员主页
def cpindex(request):
	return render(request, 'cpindex.html')


# 产品开发主页
def kfindex(request):
	return render(request, 'kfindex.html')


# 注册
def zhuce(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				username = request.POST.get("username")
				password = request.POST.get("password")
				firstname = request.POST.get("firstname")
				deptid = request.POST.get("deptid")
				lastname = request.POST.get("lastname")
				projectid = request.POST.get("projectid")
				email = request.POST.get("email")
				print(username)
				print(password)
				print(firstname)
				print(deptid)
				print(lastname)
				print(projectid)
				if projectid == '':
					projectid = 0
					print('kong')
				if lastname == '':
					lastname = 0
					print('kong')
				try:
					User.objects.create_user(username=username, password=password, first_name=firstname, deptid=deptid,
					                         last_name=lastname, projectid=projectid, email=email)
					print('用户创建成功')
					print(username)
					return render(request, 'tzsucess.html')
				except:
					projuctlist = Project.objects.all()
					deptdlist = Deptd.objects.all()
					jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
					return render(request, 'zhuce.html', locals())
			
			
			else:
				projuctlist = Project.objects.all()
				deptdlist = Deptd.objects.all()
				jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
				return render(request, 'zhuce.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 登录
def denglu(request):
	# ICP_NO = '粤ICP备2021161430号'
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		# print(username)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			# print('登录成功')
			if user.last_name == '系统管理员':
				return HttpResponseRedirect(root_url + '/index/')
			elif user.last_name == '项目开发人员':
				return HttpResponseRedirect(root_url + '/index/')
			elif user.last_name == '产品管理员':
				return HttpResponseRedirect(root_url + '/index/')
			elif user.last_name == '产品开发人员':
				return HttpResponseRedirect(root_url + '/index/')
		else:
			msg = '账号或密码错误'
			return render(request, 'login.html', locals())
	else:
		return render(request, 'login.html', locals())


# 退出
def exitd(request):
	logout(request)
	return HttpResponseRedirect(root_url + '/index/')


# 添加部门表
def appdept(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				deptname = request.POST.get('deptname')
				userid = request.POST.get('userid')
				try:
					Deptd.objects.create(deptname=deptname, user_id=userid)
					return render(request, 'tzbumensucess.html')
				except:
					
					return HttpResponseRedirect(root_url + '/appdept/')
			
			else:
				userlist = User.objects.all()
				return render(request, 'appdept.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 查看部门表
def showdept(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			deptdlist = Deptd.objects.all()
			userlist = User.objects.all()
			return render(request, 'showdept.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/jshowdept/')
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 仅查看部门表
def jshowdept(request):
	user = request.user
	if user.is_authenticated:
		deptdlist = Deptd.objects.all()
		userlist = User.objects.all()
		return render(request, 'jshowdept.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 修改部门表
def updetp(request, deptdid):
	if request.POST:
		
		deptname = request.POST.get('deptname')
		userid = request.POST.get('userid')
		Deptd.objects.filter(deptid=deptdid).update(deptname=deptname, user_id=userid)
		deptd = Deptd.objects.get(deptid=deptdid)
		userlist = User.objects.all()
		return HttpResponseRedirect(root_url + '/showdept/')
	else:
		deptd = Deptd.objects.get(deptid=deptdid)
		userlist = User.objects.all()
		return render(request, 'updept.html', locals())


# 添加产品表
def appproduct(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				pname = request.POST.get('pname')
				userid = request.POST.get('userid')
				pdescribe = request.POST.get('pdescribe')
				projectid = request.POST.get('projectid')
				# print(projectid)
				if pname == '' or userid == '':
					userlist = User.objects.filter(last_name='产品管理员')
					return render(request, 'appproduct.html', locals())
				try:
					Product.objects.create(name=pname, user_id=userid, pdescribe=pdescribe, projectid=projectid)
					return render(request, 'tzappproduct.html')
				except:
					return HttpResponseRedirect(root_url + '/appproduct/')
			
			else:
				userlist = User.objects.filter(last_name='产品管理员')
				projectlist = Project.objects.all()
				
				return render(request, 'appproduct.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 显示产品表
def showproduct(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			productlist = Product.objects.all()
			userlist = User.objects.all()
			paged = Paginator(productlist, 10)
			try:
				page = int(request.GET.get('page', 1))
				productlist = paged.page(page)
			except:
				productlist = paged.page(1)
			
			content = {}
			content['productlist'] = productlist
			return render(request, 'showproduct.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/jshowproduct/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 显示产品表
def jshowproduct(request):
	user = request.user
	if user.is_authenticated:
		productlist = Product.objects.all()
		userlist = User.objects.all()
		paged = Paginator(productlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			productlist = paged.page(page)
		except:
			productlist = paged.page(1)
		
		content = {}
		content['productlist'] = productlist
		return render(request, 'jshowproduct.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 修改产品表
# 修改部门表
def upproduct(request, pid):
	if request.POST:
		try:
			pname = request.POST.get('pname')
			userid = request.POST.get('userid')
			pdescribe = request.POST.get('pdescribe')
			Product.objects.filter(pid=pid).update(name=pname, user_id=userid, pdescribe=pdescribe)
			product = Product.objects.get(pid=pid)
			userlist = User.objects.all()
			return render(request, 'tzupproduct.html', locals())
		except:
			return HttpResponseRedirect(root_url + '/showproduct/')
	else:
		product = Product.objects.get(pid=pid)
		userlist = User.objects.all()
		return render(request, 'upproduct.html', locals())


# 产品版本号表-Pversion
# 版本号ID-vid
# 产品ID——Product
# 发布日期——date
# 版本类型——type
# 产品版本号——vnumber
# 添加产品版本号
def apppversion(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品管理员':
			if request.POST:
				productid = request.POST.get('productid')
				vnumber = request.POST.get('vnumber')
				type = request.POST.get('type')
				try:
					Pversion.objects.create(product_id=productid, vnumber=vnumber, type=type)
					return render(request, 'tzappbanben.html')
				except:
					
					return HttpResponseRedirect(root_url + '/apppversion/')
			
			else:
				productlist = Product.objects.filter()
				
				return render(request, 'apppversion.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 显示版本号087799


# 产品资料管理-Means
# 资料ID——id
# 资料名称——name
# 产品ID——Product
# 产品版本号——Pversion
# 资料类型——程序/样例代码/文档-type
# 资料——filepath
# 资料说明——explain
def appmeans(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品管理员':
			if request.POST:
				name = request.POST.get('name')
				productid = request.POST.get('productid')
				pversionid = request.POST.get('pversionid')
				type = request.POST.get('type')
				filepath = request.POST.get('filepath')
				explain = request.POST.get('explain')
				try:
					Means.objects.create(name=name, product_id=productid, pversion_id=pversionid, type=type,
					                     filepath=filepath, explain=explain)
					# print('添加成功')
					return HttpResponseRedirect(root_url + '/index/')
				except:
					return HttpResponseRedirect(root_url + '/appmeans/')
			else:
				productlist = Product.objects.all()
				
				return render(request, 'appmeans.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# ajax产品下拉框显示版本
# 导入JsonResponse返回json数据
from django.http import JsonResponse


def banben(request):
	productid = request.GET.get('productid')
	# print(productid)
	data = list(Pversion.objects.filter(product_id=productid).values())
	# print(data)
	return JsonResponse(data, safe=False)


# 选择部门显示 部门下项目
def xiangmu(request):
	deptid = request.GET.get('deptid')
	data = list(Project.objects.filter(deptd_id=deptid).values())
	
	return JsonResponse(data, safe=False)


def deptselect(request, deptid):
	user = request.user
	if user.is_authenticated:
		userlist = User.objects.filter(deptid=deptid)
		projuctlist = Project.objects.filter(deptd_id=deptid)
		deptdlist = Deptd.objects.all()
		paged = Paginator(userlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			userlist = paged.page(page)
		except:
			userlist = paged.page(1)
		content = {}
		content['userlist'] = userlist
		jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
		if user.last_name == '系统管理员':
			return render(request, 'showuser.html', locals())
		else:
			return render(request, 'jshowuser.html', locals())
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def projectselect(request, projectid):
	user = request.user
	if user.is_authenticated:
		
		userlist = User.objects.filter(projectid=projectid)
		projuctlist = Project.objects.filter(id=projectid)
		deptdlist = Deptd.objects.all()
		paged = Paginator(userlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			userlist = paged.page(page)
		except:
			userlist = paged.page(1)
		content = {}
		content['userlist'] = userlist
		jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
		if user.last_name == '系统管理员':
			return render(request, 'showuser.html', locals())
		else:
			return render(request, 'jshowuser.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def jueseselect(request, juese):
	user = request.user
	if user.is_authenticated:
		
		userlist = User.objects.filter(last_name=juese)
		projuctlist = Project.objects.all()
		deptdlist = Deptd.objects.all()
		paged = Paginator(userlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			userlist = paged.page(page)
		except:
			userlist = paged.page(1)
		content = {}
		content['userlist'] = userlist
		jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
		if user.last_name == '系统管理员':
			return render(request, 'showuser.html', locals())
		else:
			return render(request, 'jshowuser.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 上传文件 添加资料管理
def fileupload(request):
	user = request.user
	if user.is_authenticated:
		if request.method == 'POST':
			name = request.POST.get('name')
			productid = request.POST.get('productid')
			pversionid = request.POST.get('pversionid')
			type = request.POST.get('type')
			filepaths = []
			explain = request.POST.get('explain')
			# print(name)
			# print(productid)
			
			files = request.FILES.getlist('filepath')
			# print(pversionid)
			# print(files)
			
			for file in files:
				filename = file.name
				filetype = filename.split('.')[-1]
				# print(filename)
				# print(filetype)
				uploadpath = "app/static/file"
				if not os.path.exists(uploadpath):
					os.mkdir(uploadpath)
				uploadname = str(uuid.uuid1()) + "." + filetype
				path = uploadpath + os.sep + uploadname
				with open(path, "wb+") as fp:
					for chunk in file.chunks():
						fp.write(chunk)
				
				filepath = "/django/static/file/" + uploadname
				
				Means.objects.create(name=name, product_id=productid, pversion_id=pversionid, type=type,
				                     filepath=uploadname,
				                     explain=explain)
				# print('添加成功')
				
				describedd = user.first_name + '上传:' + name + '版本文件成功'
				Dongtai.objects.create(name=user.first_name, describe=describedd, date=datetime.datetime.now())
			return HttpResponseRedirect(root_url + '/index/')
		else:
			return HttpResponseRedirect(root_url + '/appmeans/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def showmiaoshu(request, mid):
	meansexp = Means.objects.get(id=mid)
	return render(request, 'showmeansexp.html', locals())


def showmeans(request):
	productlist = Product.objects.all()
	return render(request, 'showmeans.html', locals())


# ajax产品下拉框显示版本
# 导入JsonResponse返回json数据
from django.http import JsonResponse


def wenjiandd(request):
	pversionid = request.GET.get('pversionid')
	# print(pversionid)
	data = list(Means.objects.filter(pversion_id=pversionid).values())
	# print(data)
	return JsonResponse(data, safe=False)


def meanswj(request):
	meansid = request.GET.get('meansid')
	# print(meansid)
	mm = Means.objects.filter(id=meansid).values('filepath')
	for ii in mm:
		# print(ii)
		kk = ii['filepath']
	data = list(Means.objects.filter(id=meansid).values('filepath'))
	# print(data)
	return JsonResponse(data, safe=False)


# 问题标题:<input name="mtitle"><br>
#     产品名称:<input name="pid"><br>
#     产品版本号:<input name="pversionid"><br>
#     产品模块:<input name="model"><br>
#     严重程度:<input name="extent"><br>
#     要求解决日期:<input name="solvedate"><br>
#     问题描述：<textarea name="describe"></textarea>
#     提出项目组:<input name="pid"><br>
#     问题提交日期:<input name="mdate"><br>
def appmatter(request):
	user = request.user
	if user.is_authenticated:
		user = request.user
		if user.last_name == '项目开发人员':
			if request.POST:
				mtitle = request.POST.get('mtitle')
				pid = request.POST.get('pid')
				pversionid = request.POST.get('pversionid')
				model = request.POST.get('model')
				extent = request.POST.get('extent')
				describe = request.POST.get('describe')
				solvedate = request.POST.get('solvedate')
				proid = request.POST.get('proid')
				quid = request.POST.get('quid')
				print(mtitle)
				
				try:
					Matter.objects.create(mtitle=mtitle, pid=pid, pversion_id=pversionid, model=model, extent=extent,
					                      solvedate=solvedate,
					                      describe=describe, proid=proid, quid=quid, state='待分配',
					                      mdate=datetime.datetime.now())
					print('添加成功')
					discribedd = '添加问题:' + mtitle
					Dongtai.objects.create(name=user.first_name, describe=discribedd, date=datetime.datetime.now())
					return HttpResponseRedirect(root_url + '/index/')
				except:
					return HttpResponseRedirect(root_url + '/appmatter/')
			
			else:
				productlist = Product.objects.all()
				projectlist = Project.objects.all()
				
				return render(request, 'appmatter.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 显示问题表
def showmatter(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品管理员':
			matterlist = Matter.objects.all()
			projectlist = Project.objects.all()
			productlist = Product.objects.all()
			pversionlist = Pversion.objects.all()
			userlist = User.objects.all()
			return render(request, 'showmatter.html', locals())
		if user.last_name == '项目开发人员':
			return HttpResponseRedirect(root_url + '/qshowmatter/')
		if user.last_name == '产品开发人员':
			return HttpResponseRedirect(root_url + '/kshowmatter/')
		
		else:
			return HttpResponseRedirect(root_url + '/jshowmatter/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def kshowmatter(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品开发人员':
			matterlist = Matter.objects.all()
			projectlist = Project.objects.all()
			productlist = Product.objects.all()
			pversionlist = Pversion.objects.all()
			userlist = User.objects.all()
			return render(request, 'kshowmatter.html', locals())
		if user.last_name == '项目开发人员':
			return HttpResponseRedirect(root_url + '/qshowmatter/')
		
		else:
			return HttpResponseRedirect(root_url + '/jshowmatter/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 仅显示问题表
def jshowmatter(request):
	matterlist = Matter.objects.all()
	projectlist = Project.objects.all()
	productlist = Product.objects.all()
	pversionlist = Pversion.objects.all()
	userlist = User.objects.all()
	return render(request, 'jshowmatter.html', locals())


# 显示确认问题表
def qshowmatter(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '项目开发人员':
			matterlist = Matter.objects.all()
			projectlist = Project.objects.all()
			productlist = Product.objects.all()
			pversionlist = Pversion.objects.all()
			userlist = User.objects.all()
			return render(request, 'qshowmatter.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/index/')
	
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 问题表修改
import datetime


def upmatter(request, mid):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品开发人员':
			if request.POST:
				nvnumber = request.POST.get('nvnumber')
				mexplain = request.POST.get('mexplain')
				if True:
					Matter.objects.filter(mid=mid).update(nvnumber=nvnumber, mexplain=mexplain,
					                                      sdate=datetime.datetime.now())
					print('修改成功')
					Matter.objects.filter(mid=mid).update(state='已解决')
					matter = Matter.objects.get(mid=mid)
					
					describedd = user.first_name + '提交问题:' + matter.mtitle + '已经解决'
					Dongtai.objects.create(name=user.first_name, describe=describedd, date=datetime.datetime.now())
					return render(request, 'tzupmatter.html')
			else:
				matter = Matter.objects.get(mid=mid)
				projectlist = Project.objects.all()
				productlist = Product.objects.all()
				pversionlist = Pversion.objects.all()
				userlist = User.objects.all()
				return render(request, 'upmatter.html', locals())
		else:
			logout(request)
			HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def qupmatter(request, mid):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '项目开发人员':
			try:
				Matter.objects.filter(mid=mid).update(qdate=datetime.datetime.now())
				print('修改成功')
				Matter.objects.filter(mid=mid).update(state='已确认')
				matterdd = Matter.objects.get(mid=mid)
				describedd = user.first_name + '确认Bug问题:' + matterdd.mtitle + '已经确认解决'
				Dongtai.objects.create(name=user.first_name, describe=describedd, date=datetime.datetime.now())
				return render(request, 'tzqumater.html')
			except:
				return HttpResponseRedirect(root_url + '/index/')
		else:
			return HttpResponseRedirect(root_url + '/index/')
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 分配解决人
def fenpeimatter(request, mid):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '产品管理员':
			if request.POST:
				ruid = request.POST.get('ruid')
				print(ruid)
				if True:
					Matter.objects.filter(mid=mid).update(ruid=ruid)
					print('修改成功')
					Matter.objects.filter(mid=mid).update(state='已分配')
					matter = Matter.objects.get(mid=mid)
					userdd = User.objects.get(id=ruid)
					describedd = '分配问题:' + matter.mtitle + '-给:' + userdd.first_name
					Dongtai.objects.create(name=user.first_name, describe=describedd, date=datetime.datetime.now())
					return render(request, 'tzfenpei.html')
			else:
				matter = Matter.objects.get(mid=mid)
				ddii = matter.proid
				projectlist = Project.objects.all()
				productlist = Product.objects.all()
				pversionlist = Pversion.objects.all()
				deptdlist = Deptd.objects.all()
				userlist = User.objects.filter(projectid=ddii)
				print(userlist)
				return render(request, 'fenpeimatter.html', locals())
		else:
			logout()
			return HttpResponseRedirect(root_url + '/denglu/')
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 项目表添加
def appproject(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				name = request.POST.get('name')
				price = request.POST.get('price')
				deptid = request.POST.get('deptid')
				day = request.POST.get('day')
				describe = request.POST.get('describe')
				try:
					Project.objects.create(name=name, price=price, deptd_id=deptid, day=day, describe=describe, error=0
					                       )
					print('添加成功')
					return render(request, 'tzappproject.html')
				except:
					return HttpResponseRedirect(root_url + '/appproject/')
			
			else:
				deptlist = Deptd.objects.all()
				return render(request, 'appproject.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 显示项目表
def showproject(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			projectlist = Project.objects.all()
			deptdlist = Deptd.objects.all()
			paged = Paginator(projectlist, 10)
			try:
				page = int(request.GET.get('page', 1))
				projectlist = paged.page(page)
			except:
				projectlist = paged.page(1)
			
			content = {}
			content['projectlist'] = projectlist
			return render(request, 'showproject.html', locals())
		
		else:
			
			return HttpResponseRedirect(root_url + '/jshowproject/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 修改项目
# 显示项目表
def jshowproject(request):
	user = request.user
	if user.is_authenticated:
		projectlist = Project.objects.all()
		deptdlist = Deptd.objects.all()
		paged = Paginator(projectlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			projectlist = paged.page(page)
		except:
			projectlist = paged.page(1)
		
		content = {}
		content['projectlist'] = projectlist
		return render(request, 'jshowproject.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def upproject(request, pid):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				name = request.POST.get('name')
				price = request.POST.get('price')
				deptid = request.POST.get('deptid')
				day = request.POST.get('day')
				describe = request.POST.get('describe')
				if True:
					Project.objects.filter(id=pid).update(name=name, price=price, deptd_id=deptid, day=day,
					                                      describe=describe)
					print('修改成功')
					return HttpResponseRedirect(root_url + '/showproject/')
			else:
				project = Project.objects.get(id=pid)
				deptdlist = Deptd.objects.all()
				return render(request, 'upproject.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 查询用户表
def showuser(request):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			userlist = User.objects.all()
			projuctlist = Project.objects.all()
			deptdlist = Deptd.objects.all()
			paged = Paginator(userlist, 10)
			try:
				page = int(request.GET.get('page', 1))
				userlist = paged.page(page)
			except:
				userlist = paged.page(1)
			
			content = {}
			content['userlist'] = userlist
			jueselist = ['系统管理员', '项目开发人员', '产品开发人员', '产品管理员']
			return render(request, 'showuser.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/jshowuser/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 查询用户表
def jshowuser(request):
	user = request.user
	if user.is_authenticated:
		userlist = User.objects.all()
		projuctlist = Project.objects.all()
		deptdlist = Deptd.objects.all()
		paged = Paginator(userlist, 10)
		try:
			page = int(request.GET.get('page', 1))
			userlist = paged.page(page)
		except:
			userlist = paged.page(1)
		
		content = {}
		content['userlist'] = userlist
		return render(request, 'jshowuser.html', locals())
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 修改用户信息
def upuser(request, uid):
	user = request.user
	if user.is_authenticated:
		if user.last_name == '系统管理员':
			if request.POST:
				password = request.POST.get('password')
				firstname = request.POST.get('firstname')
				email = request.POST.get('email')
				deptdid = request.POST.get('deptdid')
				juese = request.POST.get('juese')
				projectid = request.POST.get('projectid')
				if projectid == '':
					projectid = 0
				
				if password == '':
					User.objects.filter(id=uid).update(first_name=firstname, email=email, deptid=deptdid,
					                                   last_name=juese, projectid=projectid)
					userlist = User.objects.filter(id=uid)
					uid = uid
					deptdlist = Deptd.objects.all()
					projectlist = Project.objects.all()
					jueselist = ['系统管理员', '项目开发人员', '产品管理员', '产品开发人员']
					return render(request, 'tzupuser.html', locals())
				else:
					user = User.objects.get(id=uid)
					user.set_password(password)
					user.save()
					User.objects.filter(id=uid).update(first_name=firstname, deptid=deptdid, last_name=juese,
					                                   projectid=projectid)
					userlist = User.objects.filter(id=uid)
					deptdlist = Deptd.objects.all()
					projectlist = Project.objects.all()
					jueselist = ['系统管理员', '项目开发人员', '产品管理员', '产品开发人员']
					return render(request, 'tzupuser.html', locals())
			
			else:
				userlist = User.objects.filter(id=uid)
				deptdlist = Deptd.objects.all()
				projectlist = Project.objects.all()
				jueselist = ['系统管理员', '项目开发人员', '产品管理员', '产品开发人员']
				return render(request, 'upuser.html', locals())
		else:
			logout(request)
			return HttpResponseRedirect(root_url + '/denglu/')
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


def gerenxinxi(request, uid):
	user = request.user
	if user.is_authenticated:
		if request.POST:
			password = request.POST.get('password')
			firstname = request.POST.get('firstname')
			email = request.POST.get('email')
			
			if password == '':
				User.objects.filter(id=uid).update(first_name=firstname, email=email)
				userlist = User.objects.filter(id=uid)
				deptdlist = Deptd.objects.all()
				projectlist = Project.objects.all()
				jueselist = ['系统管理员', '项目开发人员', '产品管理员', '产品开发人员']
				return render(request, 'tzxiugaigerenxinxi.html', locals())
			
			else:
				user = User.objects.get(id=uid)
				user.set_password(password)
				user.save()
				User.objects.filter(id=uid).update(first_name=firstname, email=email)
				logout(request)
				return HttpResponseRedirect(root_url + '/denglu/')
		
		else:
			userlist = User.objects.filter(id=uid)
			deptdlist = Deptd.objects.all()
			projectlist = Project.objects.all()
			jueselist = ['系统管理员', '项目开发人员', '产品管理员', '产品开发人员']
			return render(request, 'gerenxinxi.html', locals())
	
	else:
		return HttpResponseRedirect(root_url + '/denglu/')


# 文件下载
def wenjianxiazai(request):
	return render(request, 'wenjianxiazai.html')


from django.http import StreamingHttpResponse


def filexiazai2(request, filename):
	filepath = os.getcwd() + '/app/static/file/' + filename
	
	def fileiter(path, chunk=512):
		with open(path, 'rb')as filed:
			while True:
				content = filed.read(chunk)
				if content:
					yield content
				else:
					break
	
	response = StreamingHttpResponse(fileiter(filepath))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename={0}'.format(filename)
	return response


# 创建用户成功跳转
def tzsucess(request):
	return render(request, 'tzsucess.html')


def goajax(request, username):
	userlist = User.objects.all()
	flag = 'true'
	for uu in userlist:
		if username == uu.username:
			flag = 'false'
	return HttpResponse(flag)
