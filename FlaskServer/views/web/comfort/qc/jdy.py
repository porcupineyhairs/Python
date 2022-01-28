from modules.JdyHelper.JdyApi import APIUtils


class QcPicture:
	def __init__(self):
		# 排程任务表
		self.api_key = 'VS36bkmmx2lvdlIf3mafUcej1XGidfHo'
		self.appId = '6194c4bb3cfec400088254bb'
		self.entryId = '6194c4c12090ab0007f39968'
		
		self.api = APIUtils(self.appId, self.entryId, self.api_key)
	
	def get_picture(self, wlno):
		self.__init__()
		# 按条件获取表单数据
		title = ['wlno', 'wlno_name', 'wlno_spec', 'picture']
		
		data_filter = {
			'rel': 'and',
			'cond': [
				self.api.set_dict_filter('wlno', 'eq', wlno),
			]
		}
		data = self.api.get_form_data('', 1, title, data_filter)
		
		html_str = '''
			<!DOCTYPE html>
			<html lang="en">
			<head>
			    <meta charset="UTF-8">
			    <title>{wlno}</title>
			</head>
			<body>
			{html_body}
			</body>
			</html>
		'''
		
		html_body_str = '''
		<div>
			<img style="display: inline-block; width: 100%; max-width: 99%; height: auto;" border="2%" src="{file_url}"/>
			<label style="display: table; text-align: center;">{file_name}</label>
		</div>
		'''
		if not data:
			return html_str.format(wlno=wlno, html_body='没有获取到图片')
		else:
			for tmp in data:
				_id = tmp['_id']
				wlno = tmp['wlno']
				wlno_name = tmp['wlno_name']
				wlno_spec = tmp['wlno_spec']
				picture = tmp['picture']
				print(wlno, wlno_name, wlno_spec)
				html_body = ''
				for picture_tmp in picture:
					file_name = picture_tmp['name']
					file_url = picture_tmp['url']
					html_body += html_body_str.format(file_name=file_name, file_url=file_url)
				
				return html_str.format(wlno=wlno, html_body=html_body)
