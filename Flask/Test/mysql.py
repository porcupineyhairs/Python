import pymysql

# 打开数据库连接
db = pymysql.connect(host='192.168.0.197', user='harvey', passwd='Tiamohui', db='WG_DB', charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute(r" SELECT * FROM WG_USER ")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

print(str(data))
print(data[0][2])

# 关闭数据库连接
db.close()
