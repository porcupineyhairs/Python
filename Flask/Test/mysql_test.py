import pymysql


# # 打开数据库连接
# db = pymysql.connect(host='127.0.0.1', user='root', passwd='Tiamohui', db='WG_DB', charset='utf8')
#
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute(r" SELECT * FROM WG_USER ")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchall()
#
# print(str(data))
# print(data[0][2])
#
# # 关闭数据库连接
# db.close()

# from Module import MySql
#
# conn = ['127.0.0.1', 'root', 'Tiamohui', 'WG_DB']
# sqlstr1 = r"select u_id, u_name from wg_user order by k_id limit 10 "
# sqlstr2 = r"update wg_user set u_name = '99999' where k_id = '{0}'"
# sqlstr3 = r"delete from wg_user where k_id = '{0}'"
# mysql = MySql()
# get = mysql.Sqlwork(dataBase=conn, sqlStr=sqlstr1)
# print(get)


from Module import Sql
# connDict = ['127.0.0.1', 'root', 'Tiamohui', 'WG_DB', 'utf8']
# sqlType = 'mysql'
# sqlstr1 = r"select u_id, u_name from wg_user where k_id = '1' order by k_id limit 10 "
# sql = Sql(sqlType=sqlType, connDict=connDict)
# get = sql.SqlWork(sqlstr1, getTitle=True)
# print(get)
#
# get = sql.SqlWork(sqlstr1, getRowCount=True)
# print(get)

connDict1 = ['127.0.0.1', 'root', 'Tiamohui', 'COMFORT', 'utf8']
connDict2 = ['192.168.0.99', 'sa', 'comfortgroup2016{', 'COMFORT', 'GBK']
sql = Sql(sqlType='mysql', connDict=connDict1)
sqlstr2 = (r"SELECT CB014, CONCAT(SUBSTRING(RTRIM(CB014),1,4), '-', SUBSTRING(RTRIM(CB014), 5, 2), '-', "
           r"SUBSTRING(RTRIM(CB014), 7, 2)) FROM BOMCB "
           r"WHERE CB001 = '10010101' "
           r"AND CB005 = '3090860101'")
get = sql.SqlWork(sqlStr=sqlstr2, getTitle=True, getNoNone=False)
print(get)
