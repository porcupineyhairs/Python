from SelfModule import MsSql
from LIB.ModuleDictionary import DataBase_Dict


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
	
	get = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr.format(materials))
	if get[0] == 'None':
		get = []
	return get


def GetBomList(materials, list_tmp=None, coefficient=1.0, typeC=False, getAll=True):
	if list_tmp is None:
		list_tmp = []
	
	get = GetBomListSelect(materials=materials, typeC=typeC)
	
	for get_tmp in get:
		row_tmp = []
		if get_tmp[2] == 'P':
			row_tmp.append(get_tmp[0])
			row_tmp.append(coefficient * get_tmp[1])
			row_tmp.append(get_tmp[3])
			list_tmp.append(row_tmp)
		elif get_tmp[2] == 'C' and not getAll:
			GetBomList(get_tmp[0], list_tmp=list_tmp, coefficient=get_tmp[1], typeC=True, getAll=getAll)
		else:
			GetBomList(get_tmp[0], list_tmp=list_tmp, coefficient=get_tmp[1], getAll=getAll)
	back = list_tmp
	return back


def GetMaterialInfo(materials):
	mssql = MsSql()
	Conn_ERP = DataBase_Dict['COMFORT']
	sqlstr = (r"SELECT RTRIM(MB002), RTRIM(MB003), RTRIM(MB032), RTRIM(MB200) "
				r"FROM INVMB "
				r"WHERE MB001 = '{0}' ")
	
	get = mssql.Sqlwork(database=Conn_ERP, sqlstr=sqlstr.format(materials))
	if get[0] == 'None':
		get = []
	return get[0]
		


def GetBom(materials=None):
	if materials is None:
		return []
	else:
		get_bom = GetBomList(materials, getAll=False)
		if len(get_bom) == 0:
			return None
		else:
			for get_bom_tmp in get_bom:
				get_material = GetMaterialInfo(get_bom_tmp[0])
				for get_material_tmp in get_material:
					get_bom_tmp.append(get_material_tmp)
			return get_bom
		

def GetBomSupplier(bomList=None, supplierId=None):
	bomList_bck = bomList[:]
	bomList.clear()
	for item in bomList_bck:
		if item[5] == supplierId or item[6] == supplierId:
			bomList.append(item)
			
			
def GetMaterialSum(get=None):
	get = [['3080107017', 2.0, '0302', '平头内六角', '1/4*19/32牙长/头12.5 /煲黑+耐落', 'A0066', 'A0066'],
			['3080301002', 1.0, '0306', '弹性调整螺杆', 'SN-501/M10*297/本色', 'A0066', 'A0031'],
			['3080107017', 4.0, '0306', '平头内六角', '1/4*19/32牙长/头12.5 /煲黑+耐落', 'A0066', 'A0066'],
			['3080107015', 6.0, '0304', '平头内六角', '1/4*19/32牙长/头11厚3/煲黑+耐落', 'A0007', 'A0066'],
			['3080107017', 4.0, '0302', '平头内六角', '1/4*19/32牙长/头12.5 /煲黑+耐落', 'A0066', 'A0066'],
			['3080401031', 1.0, '0304', '插销', '￠4.5*28.5/镀锌', 'A0066', 'A0066']]

	get_bck = get[:]
	get_bck = sorted(get_bck, key=(lambda x: [x[0], x[2]]))
	get.clear()
	for get_bck_tmp in get_bck:
		print(get_bck_tmp)
		if len(get) == 0:
			get.append(get_bck_tmp)
		else:
			if get[-1][0] == get_bck_tmp[0] and get[-1][2] == get_bck_tmp[2]:
				get[-1][1] += get_bck_tmp[1]
			else:
				get.append(get_bck_tmp)
	print()
	for k in get:
		print(k)



if __name__ == '__main__':
	# get = GetBom(10710101)
	# if get is not None:
	# 	GetBomSupplier(bomList=get, supplierId='A0066')
	# 	for get_tmp in get:
	# 		print(get_tmp)
	# 	print(len(get))
	GetMaterialSum()
