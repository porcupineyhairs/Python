from SelfModule import MsSql
from LIB.ModuleDictionary import DataBase_Dict

mssql = MsSql()

k = mssql.Sqlwork(DataBase=DataBase_Dict['WG_DB'], SqlStr=r"UPDATE WG_USER SET FLAG = 'Y' WHERE U_ID = '001114'")
print(k)
