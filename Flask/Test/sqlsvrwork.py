from Module import MsSql

# ls_conn = ['40.73.246.171', 'sa', 'DGlsdnkj168', 'lserp-Ly']
ls_conn = ['192.168.0.198', 'sa', 'COMfort123456', 'test']
mssql = MsSql()

sqlstr_get0 = r"select distinct bom_no from test.dbo.test6 where err is null order by  bom_no"
sqlstr_get1 = r"select distinct wlno from test.dbo.test6 where bom_no = '{0}' order by wlno"
sqlstr_upt0 = r"update test.dbo.test6 set seq = '{2}'where bom_no = '{0}' and wlno = '{1}'"
sqlstr_upt1 = r"update test.dbo.test6 set err='Y' where bom_no = '{0}' "

get0 = mssql.Sqlwork(ls_conn, sqlstr_get0)
for get0_tmp in get0:
	get0_tmp = str(get0_tmp[0])
	print()
	print(get0_tmp)
	get1 = mssql.Sqlwork(ls_conn, sqlstr_get1.format(get0_tmp))
	get1_len = len(get1)
	print(get1_len)
	for i in range(get1_len):
		wlno_tmp = str(get1[i][0])
		print(get0_tmp, wlno_tmp, str(i + 1))
		mssql.Sqlwork(ls_conn, sqlstr_upt0.format(get0_tmp, wlno_tmp, str(i + 1)))
	mssql.Sqlwork(ls_conn, sqlstr_upt1.format(get0_tmp))
	# print(get1)
	# if get1[0] != 'None':
	# 	get1 = str(get1[0][0])
	# 	mssql.Sqlwork(ls_conn, sqlstr0_upt1.format(get0_tmp), get1)
	# else:
	# 	# mssql.Sqlwork(ls_conn, sqlstr0_upt1.format(str(get0_tmp[0]), 'err'))
	# 	pass

