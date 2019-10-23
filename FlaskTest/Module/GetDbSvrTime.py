from Module import Sql
from Module.ModuleDictionary import DataBase_Dict


class GetSvrTime:
    def __init__(self):
        self.__sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['WG_DB'])
        self.__Mode = None
        self.__Time = None
        self.__back = {
            'Time': str(None),
        }

    def GetTime(self, __get):
        self.__Mode = __get['Mode']
        if self.__Mode == 'Sort':
            __sqlstr = r"SELECT CONVERT(VARCHAR(20), GETDATE(), 112)  "

        else:
            __sqlstr = (r"SELECT (CONVERT(VARCHAR(20), GETDATE(), 112) + "
                        r"REPLACE(CONVERT(VARCHAR(20), GETDATE(), 24), ':', ''))")
        self.__Time = self.__sqlWg.SqlWork(sqlStr=__sqlstr)
        if self.__Time[0] is not None:
            self.__back['Time'] = self.__Time[0][0]
        return self.__back
