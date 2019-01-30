from SelfModule import MsSql
from LIB.ModuleDictionary import DataBase_Dict
import xlsxwriter
import numpy
import time
index = 0


# 单阶BOM明细的SQL查询
def GetBomListSelect(materials=None, typeC=False):
	mssql = MsSql()
	Conn_ERP = DataBase_Dict['COMFORT']
	sqlstr = (r"SELECT RTRIM(CB005) 品号, CAST(CB008 AS FLOAT)/CAST(CB009 AS FLOAT) 用量, "
				r"MB025 品号属性, CB011 工艺 "
				r"FROM BOMCB "
				r"INNER JOIN INVMB  ON MB001= CB005 "
				r"WHERE 1=1 "
				r"AND MB109 = 'Y' "
				r"AND (CB013 <= CONVERT(VARCHAR(20), GETDATE(), 112) OR CB013 IS NULL OR RTRIM(CB013) = '') "
				r"AND (CB014 > CONVERT(VARCHAR(20), GETDATE(), 112) OR CB014 IS NULL OR RTRIM(CB014) = '') "
				r"AND CB001 = '{0}' ")
	if typeC:
		sqlstr += r"AND CB015 = 'Y' "
	sqlstr += r"ORDER BY CB004"
	
	getList = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr.format(materials))
	if getList[0] == 'None':
		getList = []
	return getList


# BOM品号用量明细的递归循环逻辑
def GetBomList(materials, listTmp=None, coefficient=1.0, typeC=False, getAll=True):
	if listTmp is None:
		listTmp = []
		
	getList = GetBomListSelect(materials=materials, typeC=typeC)
	
	for getListTmp in getList:
		rowTmp = []
		if getListTmp[2] == 'P':
			rowTmp.append(getListTmp[0])
			rowTmp.append(coefficient * getListTmp[1])
			rowTmp.append(getListTmp[3])
			listTmp.append(rowTmp)
		elif getListTmp[2] == 'C' and not getAll:
			GetBomList(getListTmp[0], listTmp=listTmp, coefficient=getListTmp[1], typeC=True, getAll=getAll)
		else:
			GetBomList(getListTmp[0], listTmp=listTmp, coefficient=getListTmp[1], getAll=getAll)
	back = listTmp
	return back


# BOM根据品号补全品号其他信息
def GetMaterialInfo(materials):
	mssql = MsSql()
	Conn_ERP = DataBase_Dict['COMFORT']
	sqlstr = (r"SELECT RTRIM(MB004), RTRIM(MB002), RTRIM(MB003), RTRIM(MB032), RTRIM(MB200) "
				r"FROM INVMB "
				r"WHERE MB001 = '{0}' ")
	
	getList = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr.format(materials))
	if getList[0] == 'None':
		getList = []
	return getList[0]
		

# 获取BOM明细的主入口
def GetBom(materials=None):
	if materials is None:
		return []
	else:
		getBom = GetBomList(materials, getAll=False)
		if len(getBom) == 0:
			return None
		else:
			for getBomTmp in getBom:
				getMaterial = GetMaterialInfo(getBomTmp[0])
				getBomTmp.extend(getMaterial)
			return getBom
		
		
# 根据订单号获取成品品号以及订单数量
def GetOrderNumber(orderId=None):
	mssql = MsSql()
	Conn_ERP = DataBase_Dict['COMFORT']
	sqlstr = (r"SELECT RTRIM(TD004), TD008 FROM COPTD "
				r"INNER JOIN COPTC ON TC001 = TD001 AND TC002 = TD002 "
				r"WHERE 1=1 "
				r"AND TC027 = 'Y' "
				r"AND TD016 = 'N' "
				r"AND RTRIM(TD001) + '-' + RTRIM(TD002) + '-' + RTRIM(TD003) = '{0}' ")
	
	getList = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr.format(orderId))
	
	if getList[0] != 'None':
		global index
		index += 1
		print(index, '\t', orderId, '\t', getList[0][0], '\t', float(getList[0][1]))
		return getList[0][0], float(getList[0][1])


# 根据订单数量乘以BOM数量
def GetOrderSum(getList=None, coefficient=1.0):
	if getList is not None:
		for index in range(len(getList)):
			getList[index][1] = getList[index][1] * coefficient
		

def GetBomSupplier(bomList=None, supplierId=None):
	bomListBck = bomList[:]
	bomList.clear()
	for item in bomListBck:
		if item[6] == supplierId or item[7] == supplierId:
			bomList.append(item)


# 二维列表列筛选、复制，可复用
def GetNewList(getList=None, colList=None):
	if len(numpy.array(getList).shape) == 2:
		if colList is not None:
			getListBck = getList[:]
			getList.clear()
			for getListBckTmp in getListBck:
				rowTmp = []
				for colListTmp in colList:
					rowTmp.append(getListBckTmp[colListTmp])
				getList.append(rowTmp)


# 二维列表的排序，可复用
def GetListSort(getList=None, key=None):
	getListBck = getList[:]
	getList.clear()
	getList.extend(sorted(getListBck, key=key))


# 二维列表根据特定列汇总，可复用
def GetMaterialSum(getList=None, cmpList=None, sumList=None):
	getListBck = getList[:]
	getList.clear()
	rowTmp2 = []
	rowTmp1 = []
	for getListBckTmp in getListBck:
		if len(getList) == 0:
			getList.append(getListBckTmp)
		else:
			rowTmp1.clear()
			rowTmp2.clear()
			for cmpListTmp in cmpList:
				rowTmp1.append(getList[-1][cmpListTmp])
				rowTmp2.append(getListBckTmp[cmpListTmp])
			if rowTmp1 == rowTmp2:
				for sumListTmp in sumList:
					getList[-1][sumListTmp] += getListBckTmp[sumListTmp]
			else:
				getList.append(getListBckTmp)


# 根据订单号获取BOM列表并且筛选出对应供应商，且根据品号汇总
def GetOrderBomListBySupplier(orderList=None, supplierId=None):
	if orderList is not None:
		getList = []
		for orderListTmp in orderList:
			materials, number = GetOrderNumber(orderId=orderListTmp)
			getListTmp = GetBom(materials=materials)
			if getListTmp is None:  # 不存在BOM，即为原材料，取量为1，后乘以订单量
				getListTmp = [[materials, 1.0, '']]
				getListTmp[0].extend(GetMaterialInfo(materials=materials))
			GetOrderSum(getList=getListTmp, coefficient=number)
			getList.extend(getListTmp)
		
		if getList is not None:
			GetBomSupplier(bomList=getList, supplierId=supplierId)
			GetNewList(getList=getList, colList=[0, 1, 3, 4, 5, 6, 7])
			GetListSort(getList=getList, key=(lambda x: x[0]))
			GetMaterialSum(getList=getList, cmpList=[0, 2], sumList=[1])
			return getList
		else:
			return None
	else:
		return None
	
	
def GetOrderTmp():
	mssql = MsSql()
	Conn_ERP = DataBase_Dict['COMFORT']
	sqlstr = (r"SELECT RTRIM(TD001) + '-' + RTRIM(TD002) + '-' + RTRIM(TD003), TD004, TD008, TD013 FROM COPTD "
				r"INNER JOIN COPTC ON TD001 = TC001 AND TD002 = TC002 "
				r"AND TD013 BETWEEN '20190211' AND '20190415' "
				r"AND TD008 != 0 "
				r"AND TC027 = 'Y' "
				r"AND TD016 = 'N' "
				r"ORDER BY TD013, RTRIM(TD001) + '-' + RTRIM(TD002) + '-' + RTRIM(TD003)")
	
	getList = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr)
	if getList[0] == 'None':
		getList = []
	else:
		getListBck = getList[:]
		getList.clear()
		for getListBckTmp in getListBck:
			getList.append(getListBckTmp[0])
	return getList


def WriteFileTxt(Name='', getList=None):
	if len(numpy.array(getList).shape) == 2:
		getListBck = getList[:]
		getList.clear()
		for getListBckTmp in getListBck:
			strTmp = ''
			for rowTmp in getListBckTmp:
				strTmp += str(rowTmp) + '\t'
			strTmp += '\n'
			getList.append(strTmp)
	elif len(numpy.array(getList).shape) == 1:
		pass
	else:
		return 
	f = open(str(Name) + ".txt", 'a+')
	f.writelines(getList)
	f.close()
	

def WriteFileExcel(fileName=None, getList=None):
	if fileName is None or getList is None:
		return
	else:
		test_book = xlsxwriter.Workbook('./' + fileName + '.xlsx')
		worksheet = test_book.add_worksheet('Sheet1')
		bold = test_book.add_format({'bold': True})
		row = 0
		for getListTmp in getList:
			for col in range(len(getListTmp)):
				if row == 0:
					worksheet.write(row, col, getListTmp[col], bold)
				else:
					if col == 1:
						worksheet.write_number(row, col, getListTmp[col])
					else:
						worksheet.write(row, col, getListTmp[col])
			row += 1
		test_book.close()


if __name__ == '__main__':
	# # orderList = ['2210-064706-0001', '2205-064904-0001', '2214-0161-0001', '2205-064946-0001']
	# orderList = ['2205-064917-0001']
	# orderList = ['2201-015556-0010', '2203-19010008-0004']
	
	orderList = GetOrderTmp()
	
	print('订单共有', str(len(orderList)), '笔记录！')
	print('开始时间：', time.ctime())

	getList = GetOrderBomListBySupplier(orderList=orderList, supplierId='A0106')
	print(len(getList))
	
	newList = [['物料品号', '数量', '计数单位', '品名', '规格', '主供应商', '次供应商']]
	newList.extend(getList)
	WriteFileExcel(fileName='wl', getList=newList)
	print('结束时间：', time.ctime())
