from Module import Sql
from Module import DataBase_Dict
import xlsxwriter
import numpy

connStr = DataBase_Dict['Ls']
sql = Sql(connDict=DataBase_Dict['Ls'], sqlType='mssql')

sqlstr_scd = (r"select scdh, wlno, name, spec, convert(varchar(20), sl), bz, "
              r"convert(varchar(20), scrq, 23), convert(varchar(20), scjq, 23) "
              r"from mf_wwd where shbz = 1 and convert(varchar(20), scrq, 112) >= '20190501' "
              r"and convert(varchar(20), scrq, 112) < '20190701' "
              r"order by scrq, scdh")

sqlstr_wlno = r"select wlno, name, spec, convert(varchar(20), bomsl) from tf_scd where scd_no = '{0}' order by seq"

sqlstr_bom = r"select wlno, name, spec, convert(varchar(20), bomsl) from tf_bom where bom_no = '{0}' order by seq"


def Main():
	get = []
	
	get_scd = sqlWork(sqlStr=sqlstr_scd)
	for rowIndex in range(len(get_scd)):
		# print(get_scd[rowIndex])
		get_wlno = sqlWork(sqlStr=sqlstr_wlno.format(get_scd[rowIndex][0]))
		get_bom = sqlWork(sqlStr=sqlstr_bom.format(get_scd[rowIndex][1]))
		for get_wlnoTmp in get_wlno:
			# print(get_wlnoTmp)
			getTmp = get_scd[rowIndex][:]
			getTmp.extend(get_wlnoTmp)
			for get_bomTmp in get_bom:
				# print(get_bomTmp)
				if get_wlnoTmp[0] == get_bomTmp[0]:
					getTmp.extend(get_bomTmp)
					get_bom.remove(get_bomTmp)
				
				if len(get_bom) != 0:
					if get_bomTmp == get_bom[-1]:
						getTmp.extend(['', '', '', ''])
			
			get.append(getTmp)
		
		for get_bomTmp in get_bom:
			getTmp = get_scd[rowIndex][:]
			getTmp.extend(['', '', '', ''])
			getTmp.extend(get_bomTmp)
			get.append(getTmp)
	
	kk = ['生产单号', '主件品号', '主件品号', '主件规格', '生产数量', '生产单备注', '生产日期', '生产交期', '材料品号',
	      '生产单材料品名', '生产单材料对各', '生产单用量', 'BOM材料品号', 'BOM材料品名', 'BOM材料规格', 'BOM用量']
	get.insert(0, kk)
	
	# WriteFileExcel(fileName='aaa', getList=get)
	WriteFileTxt(Name='aa', getList=get)


def sqlWork(sqlStr=None, count=0):
	if count < 3:
		count += 1
		try:
			return sql.SqlWork(sqlStr=sqlStr)
		except:
			return sqlWork(sqlStr=sqlStr, count=count)
	else:
		return sql.SqlWork(sqlStr=sqlStr)
	

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
		

def WriteFileTxt(Name='', getList=None):
	# if len(numpy.array(getList).shape) == 2:
	# 	getListBck = getList[:]
	# 	getList.clear()
	# 	for getListBckTmp in getListBck:
	# 		strTmp = ''
	# 		for rowTmp in getListBckTmp:
	# 			strTmp += str(rowTmp) + '\t'
	# 		strTmp += '\n'
	# 		getList.append(strTmp)
	# elif len(numpy.array(getList).shape) == 1:
	# 	pass
	# else:
	# 	return
	f = open(str(Name) + ".txt", 'a+')
	for getListTmp in getList:
		f.writelines(str(getListTmp).replace('[', '').replace(']', '').replace(r"'", '') + '\n')
	f.close()
		

if '__main__' == __name__:
	Main()
