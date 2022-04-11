import pandas as pd
from appUsers.models import UserTypePermission, PermissionBase
from django.db.models import Q, F


class UserPermission:
	def __init__(self, request):
		self.request = request
		self.user = self.request.user

	def __sort_func(self, index):
		return index['id']

	def __sort(self, perm):
		# 第二次层排序
		for index in range(len(perm)):
			tmp = perm[0]
			if tmp['has_child']:
				perm.remove(tmp)
				child = tmp['child']
				if isinstance(child, list):
					child.sort(key=self.__sort_func)
					tmp.update({'child': child})
				perm.append(tmp)

		# 最外层排序
		perm.sort(key=self.__sort_func)
		return perm

	def get_perm(self):
		perm = []
		if self.user.is_superuser:
			perm = self.__perm_superuser()
		else:
			perm = self.__perm_normal()
		return self.__sort(perm)

	def __perm_normal(self):
		perm = []
		type_id = self.request.user.type_id
		permission = list(UserTypePermission.objects
		                  .filter(Q(type_id=type_id) & Q(perm__valid=1) & Q(run=1) & ~Q(perm__parent=0))
		                  .order_by('perm__parent')
		                  .values('perm__parent', 'perm__name', 'perm__show_index', 'perm__url', 'run', 'new', 'edit', 'delete', 'print', 'export', 'lock'))
		permission2 = permission.copy()
		# print(permission)
		parent = 0
		child = []

		for index in range(len(permission)):
			item = permission[index]
			parent_tmp = item['perm__parent']
			if index == 0:
				parent = parent_tmp
				child_item = {'id': item['perm__show_index'], 'title': item['perm__name'], 'has_child': False,
				              'url': item['perm__url'], 'image': ''}
				child.append(child_item)
			elif index != len(permission) - 1:
				if parent_tmp != parent:
					parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
					perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
					perm.append(perm_item)

					child.clear()
					parent = parent_tmp
					child_item = {'id': item['perm__show_index'], 'title': item['perm__name'], 'has_child': False,
					              'url': item['perm__url'], 'image': ''}
					child.append(child_item)
				else:
					child_item = {'id': item['perm__show_index'], 'title': item['perm__name'], 'has_child': False,
					              'url': item['perm__url'], 'image': ''}
					child.append(child_item)
			elif index == len(permission) - 1:
				if parent_tmp != parent:
					parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
					perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
					perm.append(perm_item)

					child.clear()
					parent = parent_tmp

				child_item = {'id': item['perm__show_index'], 'title': item['perm__name'], 'has_child': False,
				              'url': item['perm__url'], 'image': ''}
				child.append(child_item)
				parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
				perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
				perm.append(perm_item)
		return perm

	def __perm_superuser(self):
		perm = []
		permission = list(PermissionBase.objects
		                  .filter(Q(valid=1) & ~Q(parent=0))
		                  .order_by('parent')
		                  .values('parent', 'name', 'show_index', 'url'))
		permission2 = permission.copy()
		# print(permission)
		parent = 0
		child = []

		for index in range(len(permission)):
			item = permission[index]
			parent_tmp = item['parent']
			if index == 0:
				parent = parent_tmp
				child_item = {'id': item['show_index'], 'title': item['name'], 'has_child': False,
				              'url': item['url'], 'image': ''}
				child.append(child_item)
			elif index != len(permission) - 1:
				if parent_tmp != parent:
					parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
					perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
					perm.append(perm_item)

					child.clear()
					parent = parent_tmp
					child_item = {'id': item['show_index'], 'title': item['name'], 'has_child': False,
					              'url': item['url'], 'image': ''}
					child.append(child_item)
				else:
					child_item = {'id': item['show_index'], 'title': item['name'], 'has_child': False,
					              'url': item['url'], 'image': ''}
					child.append(child_item)
			elif index == len(permission) - 1:
				if parent_tmp != parent:
					parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
					perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
					perm.append(perm_item)

					child.clear()
					parent = parent_tmp

				child_item = {'id': item['show_index'], 'title': item['name'], 'has_child': False,
				              'url': item['url'], 'image': ''}
				child.append(child_item)
				parent_info = list(PermissionBase.objects.filter(id=parent).values())[0]
				perm_item = {'id': parent_info['show_index'], 'title': parent_info['name'], 'ico': parent_info['image'], 'has_child': True, 'child': child.copy()}
				perm.append(perm_item)
		return perm
