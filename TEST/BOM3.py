from MsSql import MsSqlHelper
import pandas as pd
import time

mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')

材料成品df = pd.read_excel('材料成品.xlsx')

sqlStr = "SELECT RTRIM(CA003) CA003 FROM BOMCA WHERE RTRIM(CA001) +'-'+ rtrim(CA002) = '{0}'"


def getCA003(string):
	if string.count('CA003') > 0:
		ca003 = ''
		for tmp1 in string.split(','):
			if tmp1.count('CA003') > 0:
				ca003 = tmp1.split('=')[1].replace('[', '').replace(']', '')
		return ca003
	else:
		return None


def getUpper(wlno):
	sqlStr0 = "SELECT 1 FROM INVMB WHERE MB025 = 'M' AND MB001 = '{0}' "
	if mssql.sqlWork(sqlStr0.format(wlno)) is not None:
		return [wlno]
	else:
		rtnList = []
		for index in range(len(材料成品df)):
			材料品号 = str(材料成品df.at[index, '材料品号'])
			if wlno == 材料品号:
				rtnList.append(str(材料成品df.at[index, '成品品号']))
		if len(rtnList) == 0:
			rtnList = ['']
		return rtnList


def getDd(wlno):
	sqlStr = r"SELECT RTRIM(TD001)+'-'+RTRIM(TD002)+'-'+RTRIM(TD003) AS 订单单号,TD004 AS 订单成品," \
			 r"TC003 订单日期,RTRIM(MA002) 客户,TD008 订单数量,TD012 金额 " \
			 r"FROM COPTC INNER JOIN COPTD ON TC001=TD001 AND TC002=TD002 INNER JOIN COPMA  ON TC004=MA001 " \
			 r"WHERE TC003 BETWEEN 20210728 AND 20210805 AND TD004 = '{0}' ORDER BY TC003, TD003"

	get = mssql.sqlWork(sqlStr.format(wlno))
	return get


def main():
	df0 = pd.read_excel('002.xlsx', dtype={'作业人': str})

	df_out = pd.DataFrame(columns=['BOM单号', '操作类型', '作业时间', '作业人', '姓名', '主件品号', '成品品号',
								   '订单单号', '订单品号', '订单数量', '订单金额', '客户', '订单日期'])
	out_index = 0
	for index in range(len(df0)):
		BOM单号 = str(df0.at[index, '数据主键'])
		操作类型 = df0.at[index, '操作类型']
		变更 = str(df0.at[index, '变更'])
		作业时间 = df0.at[index, '作业时间']
		作业人 = str(df0.at[index, '作业人']).rjust(6, '0')
		姓名 = str(df0.at[index, '姓名'])

		if 操作类型 == '删除' and 变更.count('CA003') > 0:

			主件品号 = getCA003(变更)

			for 成品品号 in getUpper(主件品号):

				订单list = getDd(成品品号)

				if 订单list is not None:
					for 订单list_tmp in 订单list:
						订单单号 = 订单list_tmp[0]
						订单品号 = 订单list_tmp[1]
						订单日期 = 订单list_tmp[2]
						客户 = 订单list_tmp[3]
						订单数量 = 订单list_tmp[4]
						订单金额 = 订单list_tmp[5]

						df_out.loc[out_index, 'BOM单号'] = BOM单号
						df_out.loc[out_index, '操作类型'] = 操作类型
						df_out.loc[out_index, '作业时间'] = 作业时间
						df_out.loc[out_index, '作业人'] = 作业人
						df_out.loc[out_index, '姓名'] = 姓名
						df_out.loc[out_index, '主件品号'] = 主件品号
						df_out.loc[out_index, '成品品号'] = 成品品号
						df_out.loc[out_index, '订单单号'] = 订单单号
						df_out.loc[out_index, '订单品号'] = 订单品号
						df_out.loc[out_index, '订单日期'] = 订单日期
						df_out.loc[out_index, '客户'] = 客户
						df_out.loc[out_index, '订单数量'] = 订单数量
						df_out.loc[out_index, '订单金额'] = 订单金额
						out_index += 1

				else:
					df_out.loc[out_index, 'BOM单号'] = BOM单号
					df_out.loc[out_index, '操作类型'] = 操作类型
					df_out.loc[out_index, '作业时间'] = 作业时间
					df_out.loc[out_index, '作业人'] = 作业人
					df_out.loc[out_index, '姓名'] = 姓名
					df_out.loc[out_index, '主件品号'] = 主件品号
					df_out.loc[out_index, '成品品号'] = 成品品号
					out_index += 1

	df_out.to_excel('002_out.xlsx', sheet_name='Sheet2', index=False)


if __name__ == '__main__':
	startdate = time.ctime()
	main()
	enddate = time.ctime()
	print('开始时间:' + startdate)
	print('结束时间:' + enddate)
