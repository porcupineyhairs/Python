import pandas as pd

from ErpBomHandler import ErpBom
from SqlHelper import MsSqlHelper

mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')
erp_bom = ErpBom(mssql=mssql)
# df0 = pd.read_excel('成品0.xlsx')
# df_up = erp_bom.bom_up(['24000695'])
df_up = erp_bom.bom_up(['24004481', '24000728', '24000695'])
# df = erp_bom.bom_down_pz('22000285', pz='TW-10灰 标配', clean=True)
# df = erp_bom.bom_down_pz(ph='10680101', pz='B01 W09-24银白色 120行程r滑轮', clean=True)
df_up = df_up.drop(['材料品号', '品号属性'], axis=1)
# 去重
df_up.drop_duplicates(keep='first', inplace=True)
df_up = df_up.reset_index(drop=True)
print(df_up)
# df.to_excel('成品0.xlsx', sheet_name='Sheet1', index=False)

df_last = erp_bom.wlno_pz(df_up)
df_last['客户配置层级1-品号'] = ''
df_last['客户配置层级1-品名'] = ''
df_last['客户配置层级1-规格'] = ''
df_last['客户配置层级2-品号'] = ''
df_last['客户配置层级2-品名'] = ''
df_last['客户配置层级2-规格'] = ''
df_last['客户配置层级3-品号'] = ''
df_last['客户配置层级3-品名'] = ''
df_last['客户配置层级3-规格'] = ''
df_last['客户配置层级4-品号'] = ''
df_last['客户配置层级4-品名'] = ''
df_last['客户配置层级4-规格'] = ''
df_last['椅脚层级1-品号'] = ''
df_last['椅脚层级1-品名'] = ''
df_last['椅脚层级1-规格'] = ''
df_last['椅脚层级2-品号'] = ''
df_last['椅脚层级2-品名'] = ''
df_last['椅脚层级2-规格'] = ''
df_last['椅脚层级3-品号'] = ''
df_last['椅脚层级3-品名'] = ''
df_last['椅脚层级3-规格'] = ''
df_last['椅脚层级4-品号'] = ''
df_last['椅脚层级4-品名'] = ''
df_last['椅脚层级4-规格'] = ''
df_last['椅脚层级5-品号'] = ''
df_last['椅脚层级5-品名'] = ''
df_last['椅脚层级5-规格'] = ''
for row1 in range(len(df_last)):
	print(str(row1) + '/' + str(len(df_last)))
	ph = df_last.at[row1, '品号']
	pz = df_last.at[row1, '客户配置']
	df_erp_pz = erp_bom.bom_down_pz(ph=ph, pz=pz, clean=True)
	for row2 in range(len(df_erp_pz)):
		if df_erp_pz.at[row2, 'MB002'] == '椅脚' or str(df_erp_pz.at[row2, 'MB002']).__contains__('客户配置'):

			if df_erp_pz.at[row2, 'MB002'] == '椅脚':
				# print(row2, df_erp_pz.at[row2, 'lv'], df_erp_pz.at[row2, 'MB002'])
				lv2 = df_erp_pz.at[row2, 'lv']
				for row3 in range(row2 + 1).__reversed__():
					if df_erp_pz.at[row3, 'lv'] == lv2 and lv2 > 0:
						df_last.at[row1, '椅脚层级{0}-品号'.format(lv2)] = df_erp_pz.at[row3, 'MD003']
						df_last.at[row1, '椅脚层级{0}-品名'.format(lv2)] = df_erp_pz.at[row3, 'MB002']
						df_last.at[row1, '椅脚层级{0}-规格'.format(lv2)] = df_erp_pz.at[row3, 'MB003']
						lv2 -= 1
						if lv2 == 0:
							break

			if str(df_erp_pz.at[row2, 'MB002']).__contains__('客户配置'):
				# print(row2, df_erp_pz.at[row2, 'lv'], df_erp_pz.at[row2, 'MB002'])
				lv2 = df_erp_pz.at[row2, 'lv']
				for row3 in range(row2 + 1).__reversed__():
					if df_erp_pz.at[row3, 'lv'] == lv2 and lv2 > 0:
						df_last.at[row1, '客户配置层级{0}-品号'.format(lv2)] = df_erp_pz.at[row3, 'MD003']
						df_last.at[row1, '客户配置层级{0}-品名'.format(lv2)] = df_erp_pz.at[row3, 'MB002']
						df_last.at[row1, '客户配置层级{0}-规格'.format(lv2)] = df_erp_pz.at[row3, 'MB003']
						lv2 -= 1
						if lv2 == 0:
							break

print(df_last)
df_last.to_excel('成品物料明细.xlsx', sheet_name='Sheet1', index=False)
