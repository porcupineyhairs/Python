from Module import MsSql
from Module.ModuleDictionary import DataBase_Dict


class GetSvrTime():
    def __init__(self):
        self.__mssql = MsSql()
        self.__WG_Conn = DataBase_Dict['WG_DB']
        self.__Time = None
        self.__back = {
            'Time': str(None),
        }

    def GetTime(self, __json):
        __sqlstr = r"SELECT CONVERT(VARCHAR(20), GETDATE(), 112)  "
        self.__Time = self.__mssql.Sqlwork(self.__WG_Conn, __sqlstr)
        if self.__Time[0] != 'None':
            self.__back['Time'] = self.__Time[0][0]
        return self.__back
