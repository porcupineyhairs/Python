from Module import MsSql

ls_conn = ['40.73.246.171', 'sa', 'DGlsdnkj168', 'lserp-Ly']
mssql = MsSql()

sqlstr0_get = (r"select distinct bom_no from test.dbo.test0 "
               r"where rm2 = '无此主品号' order by bom_no ")
sqlstr0_upt1 = (r"update test.db0.test0 set rm2 = '成品号为备注', rm3 = '{1}' where bom_no = '{0}' ")
# sqlstr0_upt2 = (r"update test.dbo.test0 set a3 = '{1}' where a1 = '{0}' ")

sqlstr1_get = (r"select material.wlno from material where bz = '{0}' ")
get0 = mssql.Sqlwork(ls_conn, sqlstr0_get)

for get0_tmp in get0:
	get0_tmp = str(get0_tmp[0])
	print(get0_tmp)
	get1 = mssql.Sqlwork(ls_conn, sqlstr1_get.format(get0_tmp))
	print(get1)
	if get1[0] != 'None':
		get1 = str(get1[0][0])
		mssql.Sqlwork(ls_conn, sqlstr0_upt1.format(get0_tmp), get1)
	else:
		# mssql.Sqlwork(ls_conn, sqlstr0_upt1.format(str(get0_tmp[0]), 'err'))
		pass

