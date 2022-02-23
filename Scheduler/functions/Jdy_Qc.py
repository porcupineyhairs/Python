from modules.JdyHelper.JdyApi import APIUtils
from modules.SqlHelper import MsSqlHelper
from modules.LogHelper import logger
import datetime
import requests
import json
import time


class QcIpqcCheckHandler:
	def __doc__(self):
		return '''
		remark:
		主体设计模式:
			1.1通过循环，获取表entryId_input的数据，
			1.2获取flag1_date与update_date，时间限制在1周内，判断表单中数据是否被修改
			1.3被修改的数据行，修改flag1=0
		
			2.1.通过循环，获取填入表单的数据，逐个字段写入日志中
			2.2.获取每个表单中的所有字段，剔除未自定义命名的字段，剔除flag字段，并做好存储dict
			2.3.根据2.2中存储的字段，生成查询的字段list
			2.4.根据2.3中的字段list，获取flag1=0的数据
			2.5.将字段list中的以v开头的字段，单独制作为一个key_list，非v开头的字段制作为normal_list
			2.6.for in key_list，结合normal_list，逐个数据写入表entryId_log中
			2.7.处理完成后，修改flag1=1，flag1_date=now
			
			3.1.判断entryId_input 中数据是否被删除
		'''
		
	def __init__(self):
		# 品质，制程品质检验记录表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '6194c4bb3cfec400088254bb'
		self.entryId_input_list = [
			'62035106be97a60008607307',  # 裁床制程品质检验表0209
		]
		self.entryId_log = ''
		
		self.entryId_input = None
		self.api = None
	
	def main(self):
		self.__init__()
		for self.entryId_input in self.entryId_input_list:
			self.api = APIUtils(self.appId, self.entryId_input, self.api_key)
			# 获取表单中的所有字段
			widgets = self.api.get_form_widgets()
			print(len(widgets))
			widgets = self.widget_clean(widgets)
			print(len(widgets))
		
		
		# 按条件获取表单数据
		# title = ['order_id', 'order_type', 'plan_order_id', 'wlno_other_flag', 'plan_wlno', 'plan_dept',
		#          'plan_wlno_name']
		#
		# data_filter = {
		# 	'rel': 'or',
		# 	'cond': [
		# 		self.api.set_dict_filter('flag1', 'eq', '0'),
		# 		self.api.set_dict_filter('flag1_date', 'empty'),
		# 		self.api.set_dict_filter('wlno_other_flag', 'eq', 'Error')
		# 	]
		# }
		# data = self.api.get_form_data('', 1000, title, data_filter)
		
		# if not data:
		# 	logger.info('排程数据-填充 -- API返回无数据')
		# else:
		# 	for tmp in data:
		# 		logger.info('排程数据-填充 -- ' + str(tmp))
		# 		_id = tmp['_id']
		# 		order_id = tmp['order_id']
		#
		# 		if order_id != '':
		# 			update = {}
		
	def widget_clean(self, widgets):
		widgets = list(widgets)
		for widget in widgets:
			print(widget)
			name = widget.get('name')
			if name.startswith('_widget'):
				print(name)
				widgets.remove(widget)
		return widgets
