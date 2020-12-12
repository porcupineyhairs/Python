# 导入MSSQL功能包
from SqlHelper import MsSqlHelper

# 建立替换勾选品号映射，[原品号，新品号]
ph_list = [['3010301014', '3010301023'], 
           ['3010301015', '3010301024'], 
           ['3010301016', '3010301025'],
           ['3010301017', '3010301026'], 
           ['3010301018', '3010301027'], 
           ['3010301019', '3010301028'],
           ['3010301020', '3010301029'], 
           ['3010301021', '3010301030'], 
           ['3010301022', '3010301031']]

# 使用账号密码建立数据库连接
mssql = MsSqlHelper(host='ip', user='user', passwd='passwd', database='db')


# 主处理逻辑，程序处理主控
# 传入 配置品号，配置名
# 处理逻辑：
#   1.根据传入的配置品号，配置名，循环逐个查询原品号是否在勾选情况，若是则返回对应的上级层级码，执行2
#   2.根据1返回的层级码，因可能返回多个层级码，需对返回的上阶层级码循环逐个处理，执行3
#   3.对单一个上阶层级码处理，判断新品号是否存在当前上阶层级码的下阶，若是，执行4
#   4.上述条件成立后，则开始替换，先把新品号勾选上，再把原品号取消勾选
def work(tmp_list):
	tr1 = tmp_list[0]
	tr2 = tmp_list[1]
	print('1. ' + tr1 + '-' + tr2)
	for ph_tmp in ph_list:
		ph1 = ph_tmp[0]
		ph2 = ph_tmp[1]
		getTr3 = existTr3(tr1, tr2, ph1)
		if getTr3 is not None:
			print('2. ' + 'PH1:' + ph1 + '     TR3:' + str(getTr3))
			for tr3_tmp in getTr3:
				tr3 = tr3_tmp[0]
				print('3. ' + tr3)
				if existPh(tr1, tr2, tr3, ph2):
					print('4. ' + tr1, tr2, tr3)
					replacePh(tr1, tr2, tr3, ph1, ph2)
				else:
					print('5. not exist ph2')


# 查找是否存在已勾选的原品号
# 传入 配置品号，配置名，原品号
# 传出 所有已勾选的原品号所在的上阶层级码，即对应原品号的层级码减3位
def existTr3(tr1, tr2, ph):
	sqlStr = r"SELECT SUBSTRING(TR003, 1, LEN(TR003)-3) FROM COPTR WHERE TR001='{0}' AND TR002='{1}' AND TR009='{2}' " \
	         r"AND TR017='Y'"
	# print('existTr3: ' + sqlStr.format(tr1, tr2, ph))
	get = mssql.sqlWork(sqlStr.format(tr1, tr2, ph))
	return get


# 判断新品号是否存在上阶层级之下
# 传入 配置品号，配置名，上阶层级码，新品号
def existPh(tr1, tr2, tr3, ph):
	sqlStr = r"SELECT TR017 FROM COPTR WHERE TR001='{0}' AND TR002='{1}' AND SUBSTRING(TR003, 1, LEN(TR003)-3)='{2}' " \
	         r"AND TR009='{3}' AND TR017 = 'N' "
	# print('existPh: ' + sqlStr.format(tr1, tr2, tr3, ph))
	get = mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph))
	return True if get is not None else False


# 替换方法，先把新品号勾选，再把原品号取消勾选
# 传入 配置品号，配置名，上阶层级码，原品号，新品号
def replacePh(tr1, tr2, tr3, ph1, ph2):
	sqlStr = r"UPDATE COPTR SET TR017='{4}' " \
	         r"WHERE TR001='{0}' AND TR002='{1}' AND SUBSTRING(TR003, 1, LEN(TR003)-3)='{2}' AND TR009='{3}' "
	print('replacePh: ' + sqlStr.format(tr1, tr2, tr3, ph2, 'Y'))
	mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph2, 'Y'))
	print('replacePh: ' + sqlStr.format(tr1, tr2, tr3, ph1, 'N'))
	mssql.sqlWork(sqlStr.format(tr1, tr2, tr3, ph1, 'N'))


# 根据SQL获取需要处理的客户配置，品号、配置名
# 根据获取到的客户配置，使用循环，逐个传入到work方法运行
def main():
	sqlStr = r"SELECT RTRIM(TQ001), RTRIM(TQ002) FROM COPTQ WHERE TQ002 LIKE '%ZB%' AND TQ002 LIKE '%保友%'  " \
	         r"AND TQ006 = 'Y' " \
	         r"ORDER BY TQ001, TQ002"

	mainGet = mssql.sqlWork(sqlStr)
	if mainGet is not None:
		for tmp in mainGet:
			work(tmp)
			print()
			print()


# 程序运行入口
if __name__ == '__main__':
	main()
