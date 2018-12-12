from Module import MsSql
from Module.ModuleDictionary import DataBase_Dict


class GetSvrTime:
    def __init__(self):
        self.__mssql = MsSql()
        self.__WG_Conn = DataBase_Dict['WG_DB']
        self.__Mode = None
        self.__Time = None
        self.__back = {
            'Time': str(None),
        }

    def GetTime(self, __json):
        self.__Mode = __json['Mode']
        if self.__Mode == 'Sort':
            __sqlstr = r"SELECT CONVERT(VARCHAR(20), GETDATE(), 112)  "

        else:
            __sqlstr = r"SELECT (CONVERT(VARCHAR(20), GETDATE(), 112) + REPLACE(CONVERT(VARCHAR(20), GETDATE(), 24), ':', ''))"
        self.__Time = self.__mssql.Sqlwork(self.__WG_Conn, __sqlstr)
        if self.__Time[0] != 'None':
            self.__back['Time'] = self.__Time[0][0]
        return self.__back
